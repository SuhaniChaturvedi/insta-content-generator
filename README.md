# 🏡 Insta Content Generator

### Automate AI-powered social media content creation for real estate properties.

---

## 🚀 Overview
**Insta Content Generator** streamlines the process of creating engaging real estate social media posts using property images.  
It automates image downloading, enhancement, and AI-powered description generation using the **Google Gemini Vision API**, and produces optimized posts for **Instagram, Facebook, LinkedIn, and Twitter**.

---
DEMO-https://drive.google.com/file/d/12vVsvuqG0ZFiEU4HgjuvpNLUl_QhqrGS/view?usp=sharing
Flow-https://docs.google.com/document/d/1brkfLRa-qga_xKzCwmQaeIvlOLlEDqcKGmS3OQHVwYk/edit?usp=sharing

## ✨ Features
- 📥 **Batch Image Downloader** — Fetch multiple property images directly from URLs.  
- 🖼️ **Image Optimization** — Resize, enhance, and compress images for each platform.  
- 🤖 **AI-Generated Descriptions** — Use **Google Gemini Vision models** to craft compelling property captions.  
- 📱 **Platform-Specific Formatting** — Auto-format posts with hashtags, emojis, and CTAs tailored to each platform.  
- 📊 **Workflow Reporting & CSV Export** — Generate summaries and export all content for bulk scheduling or CRM integration.

---

## ⚙️ Setup Instructions

### 🧩 Prerequisites
- Python **3.8+**
- Google Gemini **API Key** (available via [Google AI Studio](https://aistudio.google.com/))

---

### 📦 Installation
Clone the repository by opening your terminal and running:
git clone https://github.com/SuhaniChaturvedi/insta-content-generator.git

Then navigate into the project folder using:
cd insta-content-generator

Create a virtual environment to manage dependencies:
python3 -m venv venv

Activate the virtual environment:

On macOS or Linux: use the command "source venv/bin/activate"

On Windows: use the command "venv\Scripts\activate"

Install all required dependencies by running:
pip install -r requirements.txt

Set up your environment variables:
Copy the example environment file by running:
cp .env.example .env
Then open the newly created .env file and add your Google Gemini API key like this:
GEMINI_API_KEY=your-google-gemini-api-key-here

After everything is set up, you can start the project or run the main script using:
python main.py
