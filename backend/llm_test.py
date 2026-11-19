import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found in .env file!")
else:
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents="Write a simple SQL query to retrieve all customers."
    )

    print("Gemini API is working!")
    print("\nResponse:")
    print(response.text)