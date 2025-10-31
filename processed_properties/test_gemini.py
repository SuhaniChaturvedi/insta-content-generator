from google import genai

# Direct API key (for quick test), or set as env var
client = genai.Client(api_key="AIzaSyChvVtBqpCFULwAGvwHJ2ES-x2GGyTwtJE")

# Describe your image (local path or web URL)
image_path = "prop_001/raw/image_10.jpg"


response = client.models.generate_content(
    model="gemini-2.5-pro",  # Or 'gemini-2.5-flash' (check your quota/model access)
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

print(response.candidates[0].content.parts[0].text)
