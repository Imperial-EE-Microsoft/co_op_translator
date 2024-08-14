"""
This module contains utility functions for handling images.
Functions include saving and loading bounding boxes, drawing text on images, and plotting images with bounding boxes.
"""

import os
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageStat
import matplotlib.pyplot as plt
from src.config.font_config import FontConfig

def save_bounding_boxes(image_path, bounding_boxes):
    """
    Save bounding boxes and confidence scores to a JSON file.
    
    Args:
        image_path (str): Path to the image file.
        bounding_boxes (list): List of bounding boxes and text data.
    """
    base_name = os.path.basename(image_path)
    name, _ = os.path.splitext(base_name)
    output_dir = "./bounding_boxes"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}.json")
    
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(bounding_boxes, json_file, ensure_ascii=False, indent=4)

def load_bounding_boxes(json_path):
    """
    Load bounding boxes and confidence scores from a JSON file.
    
    Args:
        json_path (str): Path to the JSON file.
        
    Returns:
        list: List of bounding boxes and text data.
    """
    with open(json_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def get_average_color(image, bounding_box):
    """
    Get the average color of a bounding box area in the image.
    
    Args:
        image (PIL.Image.Image): The image object.
        bounding_box (list): The bounding box coordinates.
        
    Returns:
        tuple: The average color (R, G, B).
    """
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    pts = [(bounding_box[i], bounding_box[i+1]) for i in range(0, len(bounding_box), 2)]
    draw.polygon(pts, fill=255)
    stat = ImageStat.Stat(image, mask)
    avg_color = tuple(int(x) for x in stat.mean[:3])
    return avg_color

def get_text_color(bg_color):
    """
    Determine the grayscale color for text based on background color.
    
    Args:
        bg_color (tuple): Background color (R, G, B).
        
    Returns:
        tuple: Text color (R, G, B).
    """
    luminance = (0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2]) / 255
    return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)

def warp_image_to_bounding_box(image, bounding_box, image_width, image_height):
    """
    Apply perspective warp to a text image to fit the bounding box.
    
    Args:
        image (numpy.ndarray): The text image array.
        bounding_box (list): The bounding box coordinates.
        image_width (int): The width of the output image.
        image_height (int): The height of the output image.
        
    Returns:
        numpy.ndarray: The warped image array.
    """
    h, w = image.shape[:2]
    src_pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst_pts = np.float32([(bounding_box[i], bounding_box[i+1]) for i in range(0, len(bounding_box), 2)])
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(image, matrix, (image_width, image_height))
    return warped

def draw_text_on_image(text, font, text_color):
    """
    Draw text onto an image with a transparent background.
    
    Args:
        text (str): The text to draw.
        font (PIL.ImageFont.ImageFont): The font object.
        text_color (tuple): The text color (R, G, B).
        
    Returns:
        PIL.Image.Image: The image with text.
    """
    size = font.getbbox(text)[2:]  # width and height of the text
    text_image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)
    draw.text((0, 0), text, font=font, fill=text_color)
    return text_image

def create_filled_polygon_mask(bounding_box, image_size, fill_color):
    """
    Create a filled polygon mask for the bounding box area.
    
    Args:
        bounding_box (list): The bounding box coordinates.
        image_size (tuple): The size of the image (width, height).
        fill_color (tuple): The fill color (R, G, B, A).
        
    Returns:
        PIL.Image.Image: The mask image.
    """
    mask_image = Image.new('RGBA', image_size, (255, 255, 255, 0))
    mask_draw = ImageDraw.Draw(mask_image)
    pts = [(bounding_box[i], bounding_box[i+1]) for i in range(0, len(bounding_box), 2)]
    mask_draw.polygon(pts, fill=fill_color)
    return mask_image

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
        bg_color = get_average_color(image, bounding_box)
        text_color = get_text_color(bg_color)
        mask_image = create_filled_polygon_mask(bounding_box, image.size, bg_color)
        image = Image.alpha_composite(image, mask_image)
        text_image = draw_text_on_image(translated_text, font, text_color)
        text_image_array = np.array(text_image)
        warped_text_image = warp_image_to_bounding_box(text_image_array, bounding_box, image.width, image.height)
        warped_text_image_pil = Image.fromarray(warped_text_image)
        image = Image.alpha_composite(image, warped_text_image_pil)
    
    output_path = os.path.join('./translated_images', os.path.basename(image_path))
    image.save(output_path)

    # Return the annotated image
    return image

def display_image(image_path, annotated_image):
    """
    Display the original image and the annotated image side by side.
    
    Args:
        image_path (str): Path to the original image file.
        annotated_image (PIL.Image.Image): The image annotated with translated text.
    """
    plt.figure(figsize=(20, 10))
    
    # Display the annotated image
    plt.subplot(1, 2, 1)
    plt.imshow(annotated_image.convert('RGB'))
    plt.title("Annotated Image with Translated Text")
    plt.axis("off")
    
    # Display the original image
    original_image = Image.open(image_path)
    plt.subplot(1, 2, 2)
    plt.imshow(original_image)
    plt.title("Original Image")
    plt.axis("off")
    
    plt.show()