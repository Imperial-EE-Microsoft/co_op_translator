import unittest
from src.utils.text_utils import gen_image_translation_prompt, remove_code_backticks, extract_yaml_lines

class TestTextUtils(unittest.TestCase):

    def setUp(self):
        self.text_data = ["Hello, world!", "This is a test."]
        self.language = "es"  # Spanish
        self.message = "```yaml\n- Hola, mundo!\n- Esto es una prueba.\n```"

    def test_gen_image_translation_prompt(self):
        prompt = gen_image_translation_prompt(self.text_data, self.language)
        self.assertIsInstance(prompt, str)
        self.assertIn("Hello, world!", prompt)
        self.assertIn("This is a test.", prompt)

    def test_remove_code_backticks(self):
        clean_message = remove_code_backticks(self.message)
        self.assertNotIn("```", clean_message)

    def test_extract_yaml_lines(self):
        yaml_lines = extract_yaml_lines(remove_code_backticks(self.message))
        self.assertIsInstance(yaml_lines, list)
        self.assertEqual(len(yaml_lines), 2)
        self.assertEqual(yaml_lines[0], "Hola, mundo!")
        self.assertEqual(yaml_lines[1], "Esto es una prueba.")

if __name__ == '__main__':
    unittest.main()
