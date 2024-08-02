"""
This module contains functions to interact with the Azure Computer Vision and Image Analysis APIs.
It provides functionalities to extract text and bounding boxes from images.
"""

import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from src.config.base import Config

def get_computervision_client(endpoint, subscription_key):
    """
    Initialize and return a Computer Vision Client.
    
    Args:
        endpoint (str): The endpoint of the Azure Computer Vision service.
        subscription_key (str): The subscription key for the Azure Computer Vision service.
    
    Returns:
        ComputerVisionClient: The initialized client.
    """
    return ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def get_image_analysis_client(endpoint, subscription_key):
    """
    Initialize and return an Image Analysis Client.
    
    Args:
        endpoint (str): The endpoint of the Azure Image Analysis service.
        subscription_key (str): The subscription key for the Azure Image Analysis service.
    
    Returns:
        ImageAnalysisClient: The initialized client.
    """
    return ImageAnalysisClient(endpoint, AzureKeyCredential(subscription_key))

def extract_line_bounding_boxes(client, image_path):
    """
    Extract line bounding boxes from an image using Azure Computer Vision.
    
    Args:
        client (ComputerVisionClient): The initialized Computer Vision client.
        image_path (str): Path to the image file.
    
    Returns:
        list: List of dictionaries containing text, bounding box coordinates, and confidence scores.
    
    Raises:
        Exception: If the OCR operation did not succeed.
    """
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

def extract_text_imageanalysis(client, image_path):
    """
    Extract text and bounding boxes from an image using Azure Image Analysis.
    
    Args:
        client (ImageAnalysisClient): The initialized Image Analysis client.
        image_path (str): Path to the image file.
    
    Returns:
        list: List of dictionaries containing text, bounding box coordinates, and confidence scores.
    
    Raises:
        Exception: If no text was recognized in the image.
    """
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
        raise Exception("No text was recognized in the image.")

def extract_text_from_image(image_path):
    """
    Extract text from an image using Azure Image Analysis client.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        list: List of dictionaries containing text, bounding box coordinates, and confidence scores.
    """
    client = get_image_analysis_client(Config.AZURE_VISION_ENDPOINT, Config.AZURE_SUBSCRIPTION_KEY)
    return extract_text_imageanalysis(client, image_path)
