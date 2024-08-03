import unittest
import os
from src.utils.image_utils import save_bounding_boxes, load_bounding_boxes, get_average_color, get_text_color, warp_image_to_bounding_box, draw_text_on_image, create_filled_polygon_mask, plot_bounding_boxes
from PIL import Image

class TestImageUtils(unittest.TestCase):

    def setUp(self):
        # Get the absolute path of the current file and project root
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.image_path = os.path.join(self.project_root, "data/images/korean.png")

        self.bounding_boxes = [{
            "text": "Test",
            "bounding_box": [10, 10, 100, 10, 100, 50, 10, 50],
            "confidence": 0.9
        }]
        self.json_path = os.path.join(self.project_root, "data/bounding_boxes/korean.json")
        self.image = Image.new('RGB', (200, 200), color = (73, 109, 137))

    def test_save_and_load_bounding_boxes(self):
        save_bounding_boxes(self.image_path, self.bounding_boxes)
        result = load_bounding_boxes(self.json_path)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('text', result[0])
        self.assertIn('bounding_box', result[0])
        os.remove(self.json_path)  # Clean up

    def test_get_average_color(self):
        avg_color = get_average_color(self.image, self.bounding_boxes[0]['bounding_box'])
        self.assertIsInstance(avg_color, tuple)
        self.assertEqual(len(avg_color), 3)

    def test_get_text_color(self):
        text_color = get_text_color((255, 255, 255))
        self.assertEqual(text_color, (0, 0, 0))

if __name__ == '__main__':
    unittest.main()
