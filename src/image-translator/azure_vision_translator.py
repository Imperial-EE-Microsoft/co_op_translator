import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from src.config.base import Config

def get_computervision_client(endpoint, subscription_key):
    return ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def get_image_analysis_client(endpoint, subscription_key):
    return ImageAnalysisClient(endpoint, AzureKeyCredential(subscription_key))

def extract_line_bounding_boxes(client, image_path):
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
    client = get_image_analysis_client(Config.AZURE_ENDPOINT, Config.AZURE_SUBSCRIPTION_KEY)
    return extract_text_imageanalysis(client, image_path)
