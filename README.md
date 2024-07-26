# image_translation_public

## Setting up the Development Environment

Follow these steps to set up a virtual environment for development:

1. Activate the virtual environment by running the command `source venv/bin/activate`.
2. Install the packages by running the command `pip install -r requirements.txt`.
3. Fill in the environment variables an `.env` file, filling in the provided `.env.template` as a guide.

Remember to activate the virtual environment every time you work on the project by running `source env/bin/activate` from the repository's root directory.

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
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── image_translator/
│   │   ├── __init__.py
│   │   ├── azure_vision_translator.py
│   ├── text_translator/
│   │   ├── __init__.py
│   │   ├── openai_translator.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_utils.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   ├── image_translator/
│   │   ├── __init__.py
│   │   ├── test_azure_vision_translator.py
│   ├── text_translator/
│   │   ├── __init__.py
│   │   ├── test_openai_translator.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── test_image_utils.py
│   └── test_integration.py
│
├── .env.template
├── .gitignore
├── NotoSans-Medium.ttf
├── README.md
├── requirements.txt
└── setup.py


```
