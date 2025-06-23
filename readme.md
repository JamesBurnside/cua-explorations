# CUA Test

Python project to test the OpenAI CUA (Computer Use Agent) model.

## Installation

```sh
poetry install
```

## Usage

### Pre-requisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/docs/#installation) installed (for dependency management)
- An Azure OpenAI account with access to the CUA model
- Create a `.env` file in the root directory based on the provided `.env.template` file.

### Running the Agent

To run the agent, you can use the following command:

```sh
poetry run python src/main.py --instructions "Your instructions to the CUA agent here"
```

### Tests

To run the tests, you can use the following command:

```sh
poetry run pytest
```
