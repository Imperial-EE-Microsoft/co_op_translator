"""
This module contains functions to interact with the Azure Computer Vision and Image Analysis APIs.
It provides functionalities to extract text and bounding boxes from images.
"""
import os
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from src.text_translator.openai_translator import translate_text
from src.utils.image_utils import plot_annotated_image

from src.config.base import Config

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

def extract_line_bounding_boxes(image_path):
    """
    Extract line bounding boxes from an image using Azure Computer Vision.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        list: List of dictionaries containing text, bounding box coordinates, and confidence scores.
    
    Raises:
        Exception: If the OCR operation did not succeed.
    """
    client = get_computervision_client()
    with open(image_path, "rb") as image_stream:
        ocr_result = client.read_in_stream(image_stream, raw=True)
    operation_location = ocr_result.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]
    while True:
        result = client.get_read_result(operation_id)
        if result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    if result.status == OperationStatusCodes.succeeded:
        read_results = result.analyze_result.read_results
        line_bounding_boxes = []
        for read_result in read_results:
            for line in read_result.lines:
                line_bounding_boxes.append({
                    "text": line.text,
                    "bounding_box": line.bounding_box,
                    "confidence": line.appearance.style.confidence if line.appearance else None
                })
        return line_bounding_boxes
    else:
        raise Exception("OCR operation did not succeed.")

def extract_text_from_image(image_path):
    """
    Extract text and bounding boxes from an image using Azure Image Analysis.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        list: List of dictionaries containing text, bounding box coordinates, and confidence scores.
    
    Raises:
        Exception: If no text was recognized in the image.
    """
    client = get_image_analysis_client()
    with open(image_path, "rb") as image_stream:
        image_data = image_stream.read()
        result = client.analyze(
            image_data=image_data,
            visual_features=[VisualFeatures.READ],
        )
    if result.read is not None:
        line_bounding_boxes = []
        for line in result.read.blocks[0].lines:
            bounding_box = [point.x for point in line.bounding_polygon] + [point.y for point in line.bounding_polygon]
            line_bounding_boxes.append({
                "text": line.text,
                "bounding_box": bounding_box,
                "confidence": line.words[0].confidence if line.words else None
            })
        return line_bounding_boxes
    else:
        # Return an empty list if no text was recognized
        return []

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
    line_bounding_boxes = extract_text_from_image(image_path)

    # Check if any text was recognized
    if not line_bounding_boxes:
        print("No text was recognized in the image.")
        return image_path  # Return the original image path if no text is found
    
    # Extract the text data from the bounding boxes
    text_data = [line['text'] for line in line_bounding_boxes]
    
    # Translate the text data into the target language
    translated_text_data = translate_text(text_data, target_language)
    
    # Annotate the image with the translated text and save the result
    annotated_image = plot_annotated_image(image_path, line_bounding_boxes, translated_text_data)
    
    # Save the annotated image and return the path
    output_path = os.path.join('./translated_images', os.path.basename(image_path))
    annotated_image.save(output_path)

    return output_path
