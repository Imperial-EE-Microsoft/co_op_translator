"""
This module contains functions to interact with the Azure Computer Vision and Image Analysis APIs.
It provides functionalities to extract text and bounding boxes from images.
"""
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from msrest.authentication import CognitiveServicesCredentials
from src.text_translator.openai_translator import translate_text
from src.config.base import Config
from src.config.font_config import FontConfig
from src.utils.image_utils import (
    get_average_color,
    get_text_color,
    create_filled_polygon_mask,
    draw_text_on_image,
    warp_image_to_bounding_box,
    save_bounding_boxes,
    plot_bounding_boxes,
)
from PIL import Image, ImageFont
import numpy as np

def get_computervision_client():
    """
    Initialize and return a Computer Vision Client.
    
    Returns:
        ComputerVisionClient: The initialized client.
    """
    endpoint = Config.AZURE_VISION_ENDPOINT
    subscription_key = Config.AZURE_SUBSCRIPTION_KEY
    return ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def get_image_analysis_client():
    """
    Initialize and return an Image Analysis Client.
    
    Returns:
        ImageAnalysisClient: The initialized client.
    """
    endpoint = Config.AZURE_VISION_ENDPOINT
    subscription_key = Config.AZURE_SUBSCRIPTION_KEY
    return ImageAnalysisClient(endpoint, AzureKeyCredential(subscription_key))

# Function to Extract Line Bounding Boxes
def extract_line_bounding_boxes(image_path):
    """
    Extract line bounding boxes from an image using Azure Analysis Client.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        list: List of dictionaries containing text, bounding box coordinates, and confidence scores.
    
    Raises:
        Exception: If the OCR operation did not succeed.
    """

    image_analysis_client = get_image_analysis_client()
    with open(image_path, "rb") as image_stream:
        image_data = image_stream.read()
        result = image_analysis_client.analyze(
            image_data=image_data,
            visual_features=[VisualFeatures.READ],
        )

    if result.read is not None:
        line_bounding_boxes = []
        for line in result.read.blocks[0].lines:
            bounding_box = []
            for point in line.bounding_polygon:
                bounding_box.append(point.x)
                bounding_box.append(point.y)
            line_bounding_boxes.append({
                "text": line.text,
                "bounding_box": bounding_box,
                "confidence": line.words[0].confidence if line.words else None
            })
        return line_bounding_boxes
    else:
        raise Exception("No text was recognized in the image.")

def plot_annotated_image(image_path, line_bounding_boxes, translated_text_list):
    """
    Plot annotated image with translated text.
    
    Args:
        image_path (str): Path to the image file.
        line_bounding_boxes (list): List of bounding boxes and text data.
        translated_text_list (list): List of translated texts.
    """
    os.makedirs('./translated_images', exist_ok=True)
    
    image = Image.open(image_path).convert('RGBA')
    
    font_size = 40
    font = ImageFont.truetype(FontConfig.NOTO_SANS_MEDIUM, font_size)
    
    for line_info, translated_text in zip(line_bounding_boxes, translated_text_list):
        bounding_box = line_info['bounding_box']

        # Get the average color of the bounding box area
        bg_color = get_average_color(image, bounding_box)
        text_color = get_text_color(bg_color)

        # Create a mask to fill the bounding box area with the background color
        mask_image = create_filled_polygon_mask(bounding_box, image.size, bg_color)

        # Composite the mask onto the image to fill the bounding box
        image = Image.alpha_composite(image, mask_image)

        # Draw the translated text onto a temporary image
        text_image = draw_text_on_image(translated_text, font, text_color)

        # Convert the text image to an array and warp it to fit the bounding box
        text_image_array = np.array(text_image)
        warped_text_image = warp_image_to_bounding_box(text_image_array, bounding_box, image.width, image.height)

        # Convert the warped text image back to PIL format and paste it onto the original image
        warped_text_image_pil = Image.fromarray(warped_text_image)
        image = Image.alpha_composite(image, warped_text_image_pil)
    
    # Save the annotated image
    output_path = os.path.join('./translated_images', os.path.basename(image_path))
    image.save(output_path)

    # Return the annotated image
    return image


def translate_image(image_path, target_language):
    """
    Translate text in an image and return the image annotated with the translated text.
    
    Args:
        image_path (str): Path to the image file.
        target_language (str): The language to translate the text into.
    
    Returns:
        str: The path to the annotated image, or the original image path if no text is detected.
    """
    # Extract text and bounding boxes from the image
    line_bounding_boxes = extract_line_bounding_boxes(image_path)

    # Check if any text was recognized
    if not line_bounding_boxes:
        print("No text was recognized in the image.")
        return image_path  # Return the original image path if no text is found
    
    # Extract the text data from the bounding boxes
    text_data = [line['text'] for line in line_bounding_boxes]
    
    # Translate the text data into the target language
    translated_text_list = translate_text(text_data, target_language)
    
    # Annotate the image with the translated text and save the result
    annotated_image = plot_annotated_image(image_path, line_bounding_boxes, translated_text_list)
    
    # Save the annotated image and return the path
    output_path = os.path.join('./translated_images', os.path.basename(image_path))
    annotated_image.save(output_path)

    return output_path

# High-level function to process an image given a list of image paths
def process_image_paths(image_paths):
    output_dir = "./bounding_boxes"
    os.makedirs(output_dir, exist_ok=True)

    for image_path in image_paths:
        if image_path.endswith((".png", ".jpg", ".jpeg")):
            print(f"Processing {image_path}")
            line_bounding_boxes = extract_line_bounding_boxes(image_path)
            if line_bounding_boxes:
                save_bounding_boxes(image_path, line_bounding_boxes)
                plot_bounding_boxes(image_path, line_bounding_boxes, display=True)