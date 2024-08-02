import unittest
from src.image_translator.azure_vision_translator import get_computervision_client, get_image_analysis_client, extract_line_bounding_boxes, extract_text_imageanalysis
from src.config.base import Config

class TestAzureVisionTranslator(unittest.TestCase):

    def setUp(self):
        self.computervision_client = get_computervision_client(Config.AZURE_VISION_ENDPOINT, Config.AZURE_SUBSCRIPTION_KEY)
        self.image_analysis_client = get_image_analysis_client(Config.AZURE_VISION_ENDPOINT, Config.AZURE_SUBSCRIPTION_KEY)
        self.image_path = "../../data/images/bicycle.png"
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
