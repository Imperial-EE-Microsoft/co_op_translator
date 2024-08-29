# translation_public

## Setting up the Development Environment

### Create a virtual environment

1. Type the following command inside your terminal to create a virtual environment named *venv*.

    ```console
    python -m venv venv
    ```

1. Type the following command inside your terminal to activate the virtual environment.

    for Windows

    ```console
    venv\Scripts\activate.bat
    ```

    for Mac / Linux

    ```console
    source venv/bin/activate
    ```

> [!NOTE]
>
> If it worked, you should see *(venv)* before the command prompt.
> Remember to activate the virtual environment every time you work on the project by running from the repository's root directory.

### Install the required packages

1. Type the following commands inside your terminal to install the required packages.

    ```console
    pip install -r requirements.txt
    ```

### Add environment variables

1. Create an `.env` file in the root directory of your project by copying the provided .env.template file. Fill in the environment variables in the `.env` file as a guide.

1. The environment variables will be automatically loaded when you run any script that imports and executes `base.py` from the `src/config` directory.

### Install the package in editable mode

1. Type the following command inside your terminal to install the package in editable mode:

    ```console
    pip install -e .
    ```

## Running Tests

1. To run tests, make sure your virtual environment is activated, then type the following command:

    ```console
    pytest tests/
    ```

## Sample notebooks

- [Getting Started with notebook: basic version](notebooks/notebook_for_microsoft_final.ipynb)
- [Getting Started with notebook: module version](notebooks/notebook_for_module_project.ipynb)
