# image_translation_public

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

1. Fill in the environment variables an `.env` file, filling in the provided `.env.template` as a guide.

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
│   └── main.py
│
├── tests/
│   ├── image_translator/
│   │   ├── test_azure_vision_translator.py
│   ├── text_translator/
│   │   ├── test_openai_translator.py
│   ├── utils/
│   │   ├── test_image_utils.py
│   └── test_integration.py
│
├── .env.template
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py

```
