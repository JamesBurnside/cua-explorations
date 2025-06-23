import argparse
import asyncio
import logging
import os

import dotenv
import cua
import local_computer
import openai
import platform

dotenv.load_dotenv()

def get_default_env():
	system = platform.system().lower()
	if system == "windows":
		return "windows"
	elif system == "darwin":
		return "macos"
	elif system == "linux":
		return "linux"
	else:
		return "windows"

def check_env():
	if "AZURE_OPENAI_ENDPOINT" not in os.environ:
		raise ValueError("Environment variable AZURE_OPENAI_ENDPOINT is not set.")
	if "AZURE_OPENAI_API_KEY" not in os.environ:
		raise ValueError("Environment variable AZURE_OPENAI_API_KEY is not set.")
	if "AZURE_OPENAI_MODEL" not in os.environ:
		raise ValueError("Environment variable AZURE_OPENAI_MODEL is not set.")
	if "AZURE_OPENAI_API_VERSION" not in os.environ:
		raise ValueError("Environment variable AZURE_OPENAI_API_VERSION is not set.")

async def main():

	logging.basicConfig(level=logging.WARNING, format="%(message)s")
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	parser = argparse.ArgumentParser()
	parser.add_argument("--instructions", dest="instructions",
		default="Open web browser and go to microsoft.com.",
		help="Instructions to give to the AI CUA Agent.")
	parser.add_argument("--autoplay", dest="autoplay", action="store_true",
		default=True, help="Autoplay actions without confirmation")

	default_env = get_default_env()

	parser.add_argument("--environment", dest="environment", default=default_env)
	args = parser.parse_args()

	client = openai.AsyncAzureOpenAI(
		azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
		api_key=os.environ["AZURE_OPENAI_API_KEY"],
		api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
	)

	model = os.environ.get("AZURE_OPENAI_MODEL")

	# Computer is used to take screenshots and send keystrokes or mouse clicks
	computer = local_computer.LocalComputer()

	# Scaler is used to resize the screen to a smaller size
	computer = cua.Scaler(computer, (1024, 768))

	# Agent to run the CUA model and keep track of state
	agent = cua.Agent(client, model, computer)

	# Get the user request
	if args.instructions:
		user_input = args.instructions
	else:
		user_input = input("Please enter the initial task: ")

	logger.info(f"User: {user_input}")
	agent.start_task()
	while True:
		if not user_input and agent.requires_user_input:
			logger.info("")
			user_input = input("User: ")
		await agent.continue_task(user_input)
		user_input = None
		if agent.requires_consent and not args.autoplay:
			input("Press Enter to run computer tool...")
		elif agent.pending_safety_checks and not args.autoplay:
			logger.info(f"Safety checks: {agent.pending_safety_checks}")
			input("Press Enter to acknowledge and continue...")
		if agent.reasoning_summary:
			logger.info("")
			logger.info(f"Action: {agent.reasoning_summary}")
		for action, action_args in agent.actions:
			logger.info(f"  {action} {action_args}")
		if agent.messages:
			logger.info("")
			logger.info(f"Agent: {"".join(agent.messages)}")

if __name__ == "__main__":
	asyncio.run(main())