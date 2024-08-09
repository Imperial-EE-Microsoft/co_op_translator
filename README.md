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

## Project Structure

```text
microsoft_translation_public/
│
├── data/
│   ├── images/
│   ├── analyzed_images/
│   ├── bounding_boxes/
│   └── translated_images/
│
├── fonts/
│   └── NotoSans-Medium.ttf
│
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── image_translator/
│   │   ├── azure_vision_translator.py
│   ├── text_translator/
│   │   ├── openai_translator.py
│   ├── utils/
│   │   ├── image_utils.py
│   │   ├── text_utils.py
│   └── main.py
│
├── tests/
│   ├── image_translator/
│   │   ├── test_azure_vision_translator.py
│   ├── text_translator/
│   │   ├── test_openai_translator.py
│   ├── utils/
│   │   ├── test_image_utils.py
│   │   ├── test_text_utils.py
│   └── integration_tests/
│       ├── integration_test.py
│
├── .env.template
├── .gitignore
├── conftest.py
├── pytest.ini
├── README.md
├── requirements.txt
├── setup.cfg
└── setup.py

```
