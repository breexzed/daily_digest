import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client()


SYSTEM_INSTRUCTION = """
You are a minimal systems intelligence engine. You will be given a raw Python dictionary containing news feed metadata. 

Your task is to rewrite the headline and description into a single, punchy, high-impact sentence. 

Rules:
- Output your response as a single plain-text paragraph.
- Do not use markdown symbols (*, #, -) or HTML tags.
- Focus entirely on structural reductionism: give me the raw signal, zero fluff.
"""

def summarize_article(raw_article_text):
    """
    Takes a raw markdown story string, passes it to the AI, 
    and returns a clean, condensed summary string.
    """
    print("Passing raw payload to LLM engine...")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
        contents=raw_article_text,
        config={"system_instruction": SYSTEM_INSTRUCTION}
        
        )
        return response.text
    except Exception as e:
        print(f"LLM Transformation failed: {e}")
        return f" [Transformation Error] Raw Snippet:\n{raw_article_text[:500]}... "
