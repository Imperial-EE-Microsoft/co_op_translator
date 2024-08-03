import unittest
import os
from src.image_translator.azure_vision_translator import get_computervision_client, get_image_analysis_client, extract_line_bounding_boxes, extract_text_imageanalysis
from src.config.base import Config

class TestAzureVisionTranslator(unittest.TestCase):

    def setUp(self):
        self.computervision_client = get_computervision_client(Config.AZURE_VISION_ENDPOINT, Config.AZURE_SUBSCRIPTION_KEY)
        self.image_analysis_client = get_image_analysis_client(Config.AZURE_VISION_ENDPOINT, Config.AZURE_SUBSCRIPTION_KEY)
        # Set the image path dynamically based on the current file's directory
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.image_path = os.path.join(self.project_root, "data/images/korean.png")

    def test_extract_line_bounding_boxes(self):
        result = extract_line_bounding_boxes(self.computervision_client, self.image_path)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('text', result[0])
        self.assertIn('bounding_box', result[0])

    def test_extract_text_imageanalysis(self):
        result = extract_text_imageanalysis(self.image_analysis_client, self.image_path)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('text', result[0])
        self.assertIn('bounding_box', result[0])

if __name__ == '__main__':
    unittest.main()
