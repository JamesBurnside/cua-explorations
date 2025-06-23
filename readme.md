# CUA Test

Python project to test the OpenAI CUA (Computer Use Agent) model.

## Usage

### Pre-requisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/docs/#installation) installed (for dependency management)
- An Azure OpenAI account with access to the CUA model
- Create a `.env` file in the root directory based on the provided `.env.template` file and substitute the placeholders with your actual Azure OpenAI credentials.

### Installation

1. Clone repository
1. Install dependencies using Poetry:

    ```sh
    poetry install
    ```

### Running the Agent

```sh
poetry run python src/main.py --instructions "Your instructions to the CUA agent here"
```

### Tests

```sh
poetry run pytest
```
