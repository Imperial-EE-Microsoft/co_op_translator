import click
from src.translators.project_translator import ProjectTranslator

@click.command()
@click.option('--language-codes', '-l', required=True, help='Space-separated language codes for translation (e.g., "es fr de").')
@click.option('--root-dir', '-r', default='.', help='Root directory of the project (default is current directory).')
def main(language_codes, root_dir):
    """
    Translate all markdown and image files in the project based on the specified language codes.
    
    Example usage:
    translate_project --language-codes "es fr de"
    translate_project --language-codes "all" --root-dir "./my_project"

    Simplified version:
    translate -l "es fr de"
    translate -l "all" -r "./my_project"
    """
    # Initialize the ProjectTranslator
    translator = ProjectTranslator(language_codes, root_dir)
    
    # Translate the project
    translator.translate_project()

    click.echo(f"Project translation completed for languages: {language_codes}")

if __name__ == '__main__':
    main()
