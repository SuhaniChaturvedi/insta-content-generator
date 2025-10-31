Insta Content Generator
Project Overview
This project automates the workflow of generating engaging social media content for real estate properties using images. It downloads property images, processes them for different social media platforms, and uses the Google Gemini AI Vision API to generate compelling descriptions. The descriptions are formatted into posts optimized for Instagram, Facebook, LinkedIn, and Twitter, then compiled into CSV exports for easy bulk posting or CRM integration.

Features
Batch download property images from URLs

Image resizing, enhancement, and compression for social media optimization

Automated AI-generated property descriptions using Google Gemini vision models

Platform-specific social post creation with formatted hashtags and key info

Workflow reporting and CSV export for integration

Setup Instructions
Prerequisites
Python 3.8+

Google Gemini API key (get from Google AI Studio)

Installation
Clone the repository:

bash
git clone https://github.com/SuhaniChaturvedi/insta-content-generator.git
cd insta-content-generator
Create and activate a virtual environment:

bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Configure your environment:

Copy .env.example to .env

bash
cp .env.example .env
Add your Gemini API key to .env:

text
GEMINI_API_KEY=your-google-gemini-api-key-here
