import unittest
from src.text_translator.openai_translator import get_openai_client, translate_text

class TestOpenAITranslator(unittest.TestCase):

    def setUp(self):
        self.client = get_openai_client()
        self.text_data = ["Hello, world!", "This is a test."]
        self.language = "ko"  # Korean

    def test_translate_text(self):
        result = translate_text(self.text_data, self.language)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], str)

if __name__ == '__main__':
    unittest.main()
