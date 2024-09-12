import logging
import click
import importlib.resources
import yaml
from co_op_translator.translators.project_translator import ProjectTranslator

@click.command()
@click.option('--language-codes', '-l', required=True, help='Space-separated language codes for translation (e.g., "es fr de").')
@click.option('--root-dir', '-r', default='.', help='Root directory of the project (default is current directory).')
@click.option('--debug', is_flag=True, help='Enable debug mode (default is INFO level, set to DEBUG if enabled).')
def main(language_codes, root_dir, debug):
    """
    Translate all markdown and image files in the project based on the specified language codes.
    
    Example usage:
    translate --language-codes "es fr de"
    translate --language-codes "all" --root-dir "./my_project"

    Simplified version:
    translate -l "es fr de"
    translate -l "all" -r "./my_project"

    To enable debug mode:
    translate --language-codes "es fr de" --debug
    translate -l "es fr de" -r "./my_project" --debug
    """

    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug mode enabled.")
    else:
        logging.basicConfig(level=logging.CRITICAL)

    # If 'all' is passed, load all language codes from the font mapping file
    if language_codes == "all":
        with importlib.resources.path('co_op_translator.fonts', 'font_language_mappings.yml') as mappings_path:
            with open(mappings_path, 'r', encoding='utf-8') as file:
                font_mappings = yaml.safe_load(file)
                language_codes = " ".join(font_mappings.keys())  # Use all keys (languages) from the font mapping file
                logging.debug(f"Loaded language codes from font mapping: {language_codes}")
    
    # Initialize the ProjectTranslator
    translator = ProjectTranslator(language_codes, root_dir)
    
    # Translate the project
    translator.translate_project()

    click.echo(f"Project translation completed for languages: {language_codes}")

if __name__ == '__main__':
    main()
