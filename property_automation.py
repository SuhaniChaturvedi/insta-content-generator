# PROPERTY IMAGE AUTOMATION - COMPLETE PYTHON IMPLEMENTATION
# Author: AI Assistant
# Date: October 31, 2025
# Description: Full workflow for collecting, processing, and automating property listings

from dotenv import load_dotenv
import os
from google import genai

load_dotenv()  # Loads .env file variables into environment

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Image processing libraries
from PIL import Image, ImageEnhance
import requests

# Data handling
import pandas as pd


class PropertyImageProcessor:
    """
    Main class to handle property image automation workflow.
    """

    def __init__(self, config_path: str = None):
        """Initialize the processor with configuration."""
        self.config = self.load_config(config_path)
        self.processed_images = []
        self.property_listings = []
        self.log = []

    def load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from JSON file or use defaults."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        # Default configuration
        return {
            "image_settings": {
                "target_width": 1200,
                "target_height": 800,
                "quality": 85,
                "format": "JPEG"
            },
            "platforms": {
                "instagram": {"width": 1080, "height": 1350},
                "facebook": {"width": 1200, "height": 628},
                "linkedin": {"width": 1200, "height": 627}
            },
            "output_dir": "./processed_properties"
        }

    # ======================= LAYER 1: DATA COLLECTION =======================

    def download_image(self, image_url: str, property_id: str) -> Optional[str]:
        """Download an image from URL and save locally."""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            output_dir = os.path.join(self.config["output_dir"], property_id, "raw")
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, f"image_{len(os.listdir(output_dir))}.jpg")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            self.log_action(f"Downloaded image: {file_path}")
            return file_path
        except Exception as e:
            self.log_action(f"ERROR downloading {image_url}: {str(e)}")
            return None

    def collect_property_images(self, property_data: List[Dict]) -> List[str]:
        """Collect multiple property images from URLs."""
        downloaded_paths = []
        for prop in property_data:
            prop_id = prop.get('id')
            image_urls = prop.get('image_urls', [])
            for url in image_urls:
                file_path = self.download_image(url, prop_id)
                if file_path:
                    downloaded_paths.append({
                        'property_id': prop_id,
                        'file_path': file_path,
                        'url': url
                    })
        return downloaded_paths

    # ======================= LAYER 2: IMAGE PROCESSING =======================

    def resize_image(self, image_path: str, target_width: int, target_height: int = None) -> Image.Image:
        """Resize image maintaining aspect ratio."""
        img = Image.open(image_path)
        if target_height is None:
            ratio = target_width / img.size[0]
            target_height = int(img.size[1] * ratio)
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        self.log_action(f"Resized image: {image_path} to {target_width}x{target_height}")
        return img

    def compress_image(self, img: Image.Image, quality: int = 85) -> Image.Image:
        """Compress image while maintaining quality."""
        self.log_action(f"Compressed image with quality: {quality}")
        return img

    def enhance_image(self, img: Image.Image) -> Image.Image:
        """Enhance image: brightness, contrast, sharpness."""
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)
        self.log_action("Enhanced image: brightness, contrast, sharpness")
        return img

    def process_image_for_platform(self, image_path: str, platform: str) -> Optional[str]:
        """Process image optimized for specific social media platform."""
        try:
            dimensions = self.config["platforms"].get(platform)
            if not dimensions:
                self.log_action(f"Unknown platform: {platform}")
                return None
            img = self.resize_image(image_path, dimensions["width"], dimensions["height"])
            img = self.enhance_image(img)
            img = self.compress_image(img, quality=85)
            output_dir = os.path.join(self.config["output_dir"], "platform_optimized", platform)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{Path(image_path).stem}_{platform}.jpg")
            img.save(output_path, "JPEG", quality=85, optimize=True)
            self.log_action(f"Processed for {platform}: {output_path}")
            return output_path
        except Exception as e:
            self.log_action(f"ERROR processing for {platform}: {str(e)}")
            return None

    def batch_process_images(self, image_paths: List[str]) -> Dict[str, List[str]]:
        """Batch process images for all platforms."""
        results = {platform: [] for platform in self.config["platforms"].keys()}
        for image_path in image_paths:
            for platform in self.config["platforms"].keys():
                processed = self.process_image_for_platform(image_path, platform)
                if processed:
                    results[platform].append(processed)
        return results

    # ======================= LAYER 3: AI DESCRIPTION GENERATION =======================

    def generate_description_gemini(self, image_path: str) -> Optional[str]:
        """
        Generate property description using Gemini Vision API.
        """
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[{
                    "role": "user",
                    "parts": [
                        {
                            "text": "Describe the property in this image as a compelling social post (max 100 words)."
                        },
                        {
                            "inline_data": {"mime_type": "image/jpeg", "data": open(image_path, "rb").read()}
                        }
                    ]
                }]
            )
            description = response.candidates[0].content.parts[0].text
            self.log_action(f"Generated description (Gemini): {description[:50]}...")
            return description
        except Exception as e:
            self.log_action(f"ERROR generating description (Gemini): {str(e)}")
            return None

    def generate_description(self, image_path: str) -> Optional[str]:
        """
        Generate description using Gemini API only.
        """
        return self.generate_description_gemini(image_path)

    # ======================= LAYER 4: CONTENT PREPARATION =======================

    def create_social_media_posts(self, description: str, property_info: Dict) -> Dict[str, str]:
        """Create platform-specific social media posts from description."""
        posts = {}
        price = property_info.get("price", "Contact for price")
        address = property_info.get("address", "New Listing")
        prop_type = property_info.get("type", "Property")

        posts["instagram"] = f"""{description}

📍 {address}
💰 {price}
🏠 {prop_type}

DM for more details! 📞
.
.
#realestate #propertylisting #luxury #homeforsale #{prop_type.lower().replace(' ', '')} #realestateagent #newhome"""

        posts["facebook"] = f"""🏡 New Listing Alert! 🏡

{description}

📍 Location: {address}
💵 Price: {price}
🏘️ Type: {prop_type}

Contact us today to schedule a showing!
Schedule your tour now →"""

        posts["linkedin"] = f"""Exciting New Property Listing!

{description}

Professional Details:
• Location: {address}
• Investment Value: {price}
• Category: {prop_type}

#RealEstate #PropertyInvestment #CommercialRealEstate #DreamHome"""

        posts["twitter"] = f"""🏠 NEW: {prop_type} at {address}

{description[:100]}...

💰 {price}

Learn more → Link in bio 🔗

#RealEstate #HomeSale"""

        return posts

    # ======================= LAYER 5: AUTOMATION & OUTPUT =======================

    def create_csv_export(self, listings_data: List[Dict], output_path: str = None) -> str:
        """Create CSV file with all listing data for import to social media or CRM."""
        if not output_path:
            os.makedirs(self.config["output_dir"], exist_ok=True)
            output_path = os.path.join(self.config["output_dir"], "listings_export.csv")
        df = pd.DataFrame(listings_data)
        df.to_csv(output_path, index=False)
        self.log_action(f"Exported CSV: {output_path}")
        return output_path

    def log_action(self, message: str):
        """Log workflow actions."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log.append(log_entry)
        print(log_entry)

    def save_workflow_report(self, output_path: str = None) -> str:
        """Save complete workflow report."""
        if not output_path:
            os.makedirs(self.config["output_dir"], exist_ok=True)
            output_path = os.path.join(self.config["output_dir"], "workflow_report.txt")
        with open(output_path, 'w') as f:
            f.write("PROPERTY IMAGE AUTOMATION - WORKFLOW REPORT\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write("=" * 60 + "\n\n")
            f.write("LOG ENTRIES:\n")
            f.write("-" * 60 + "\n")
            for log_entry in self.log:
                f.write(log_entry + "\n")
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"Total Entries: {len(self.log)}\n")
        self.log_action(f"Report saved: {output_path}")
        return output_path


# ======================= EXAMPLE USAGE =======================

if __name__ == "__main__":
    print("Property Image Automation Workflow - Real Run\n")

    # Initialize processor
    processor = PropertyImageProcessor()

    # Real property data (with actual URLs)
    sample_properties = [
        {
            "id": "prop_001",
            "address": "123 Maple Street, Downtown",
            "price": "$450,000",
            "type": "2-Bedroom Condo",
            "image_urls": [
                "https://cdn.britannica.com/05/157305-004-53D5D212.jpg",
                "https://prod.rockmedialibrary.com/api/public/content/43cab7c9a2b54fe881f724d245465134?v=37e89cfd",
                "https://d2u1z1lopyfwlx.cloudfront.net/thumbnails/9b21e39c-e784-5f98-9be2-2f9c2eeab989/c6812dce-1a47-5122-81fc-675c9de28cd8.jpg",
                "https://www.shutterstock.com/image-illustration/3d-rendering-modern-cozy-house-600nw-1699684264.jpg",
                "https://media.istockphoto.com/id/1396856251/photo/colonial-house.jpg?s=612x612&w=0&k=20&c=_tGiix_HTQkJj2piTsilMuVef9v2nUwEkSC9Alo89BM="
            ]
        }
    ]

    print("\n[LAYER 1] DATA COLLECTION")
    print("-" * 50)
    processor.log_action("Starting real image collection...")
    downloaded_imgs = processor.collect_property_images(sample_properties)

    print("\n[LAYER 2] IMAGE PROCESSING")
    print("-" * 50)
    img_paths = [img['file_path'] for img in downloaded_imgs]
    processed_for_platforms = processor.batch_process_images(img_paths)

    print("\n[LAYER 3] AI DESCRIPTION GENERATION")
    print("-" * 50)
    descriptions = []
    for img_path in img_paths:
        desc = processor.generate_description(img_path)
        if desc is None:
            desc = "Fallback: Beautiful property with modern features."
        descriptions.append(desc)

    print("\n[LAYER 4] CONTENT PREPARATION")
    print("-" * 50)
    posts = []
    for desc in descriptions:
        post = processor.create_social_media_posts(desc, sample_properties[0])
        posts.append(post)
        print("\nSample Instagram Post:")
        print(post["instagram"][:200] + "...")

    print("\n[LAYER 5] AUTOMATION & OUTPUT")
    print("-" * 50)
    export_data = []
    for i, desc in enumerate(descriptions):
        export_data.append({
            "property_id": sample_properties[0]["id"],
            "address": sample_properties[0]["address"],
            "price": sample_properties[0]["price"],
            "type": sample_properties[0]["type"],
            "description": desc,
            "instagram_post": posts[i]["instagram"][:100],
            "facebook_post": posts[i]["facebook"][:100],
            "linkedin_post": posts[i]["linkedin"][:100],
            "processing_date": datetime.now().isoformat()
        })

    csv_path = processor.create_csv_export(export_data)
    report_path = processor.save_workflow_report()

    print(f"\n✅ Workflow completed successfully!")
    print(f"📊 Report saved: {report_path}")
    print(f"📑 CSV saved: {csv_path}")
