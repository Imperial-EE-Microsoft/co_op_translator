import unittest
import os
from src.image_translator.azure_vision_translator import extract_line_bounding_boxes, extract_text_from_image

class TestAzureVisionTranslator(unittest.TestCase):

    def setUp(self):
        # Set the image path dynamically based on the current file's directory
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.image_path = os.path.join(self.project_root, "data/images/korean.png")

    def test_extract_line_bounding_boxes(self):
        result = extract_line_bounding_boxes(self.image_path)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('text', result[0])
        self.assertIn('bounding_box', result[0])

    def test_extract_text_from_image(self):
        result = extract_text_from_image(self.image_path)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('text', result[0])
        self.assertIn('bounding_box', result[0])

if __name__ == '__main__':
    unittest.main()
