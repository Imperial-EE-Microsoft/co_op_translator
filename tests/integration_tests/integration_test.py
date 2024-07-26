import os
import unittest
import json
import difflib
from src.image_translator.azure_vision_translator import extract_text_from_image
from src.text_translator.openai_translator import get_openai_client, translate_text
from src.config.base import Config

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.image_dir = "./data/images"
        self.expected_results_dir = "./data/expected_results"
        self.language = "Spanish"
        self.client = get_openai_client(Config.OPENAI_BASE, Config.OPENAI_KEY, Config.DEPLOYMENT_NAME, Config.API_VERSION)
    
    def assert_text_similarity(self, text1, text2, threshold=0.8):
        """
        Asserts that two texts are similar based on a given threshold.
        
        Args:
            text1 (str): First text.
            text2 (str): Second text.
            threshold (float): Similarity threshold between 0 and 1.
        """
        similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
        self.assertGreaterEqual(similarity, threshold, f"Texts are not similar enough: '{text1}' vs '{text2}' (similarity: {similarity:.2f})")

    def test_image_translation(self):
        for image_name in os.listdir(self.image_dir):
            if image_name.endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(self.image_dir, image_name)
                expected_result_path = os.path.join(self.expected_results_dir, f"{os.path.splitext(image_name)[0]}.json")

                with open(expected_result_path, "r", encoding="utf-8") as f:
                    expected_data = json.load(f)

                expected_extracted_text = expected_data["extracted_text"]
                expected_translated_text = expected_data["translated_text"]

                # Extract text from image
                extracted_text = extract_text_from_image(image_path)
                self.assertEqual(len(extracted_text), len(expected_extracted_text), f"Number of extracted texts does not match for image {image_name}")

                for extracted, expected in zip(extracted_text, expected_extracted_text):
                    self.assertEqual(extracted["bounding_box"], expected["bounding_box"], f"Bounding box does not match for text '{extracted['text']}' in image {image_name}")
                    self.assertAlmostEqual(extracted["confidence"], expected["confidence"], places=2, msg=f"Confidence does not match for text '{extracted['text']}' in image {image_name}")
                    self.assert_text_similarity(extracted["text"], expected["text"])

                # Translate extracted text
                translated_texts = translate_text(self.client, [text["text"] for text in extracted_text], self.language)
                self.assertEqual(len(translated_texts), len(expected_translated_text), f"Number of translated texts does not match for image {image_name}")

                for translated, expected in zip(translated_texts, expected_translated_text):
                    self.assert_text_similarity(translated, expected)

if __name__ == "__main__":
    unittest.main()
