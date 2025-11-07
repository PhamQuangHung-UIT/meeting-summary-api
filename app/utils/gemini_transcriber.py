import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
 
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError('GEMINI_API_KEY is not set in .env file')

client = genai.Client(api_key=GEMINI_API_KEY)

def transcribe_gemini(audio_bytes: bytes, file_extension: str):
    prompt = '''
    Transcribe the provided audio file verbatim, identifying different speakers based on voice changes (label them as Speaker 1, Speaker 2, etc., starting from Speaker 1 for the first voice). For each spoken segment, provide:
    - An estimated timestamp in the format "HhMmSs-start to HhMmSs-end" (e.g., "0h0m0s-0h1m4s"), based on the audio timeline.
    - The exact spoken content without any repetition, filler words (unless essential), or summarization.

    Output ONLY a valid JSON array of objects, nothing else. Do not include any introduction, explanation, or additional text. Structure each object as:
    {
        "speaker": "Speaker 1" (or Speaker 2, etc.),
        "timestamp": "0h0m0s-0h1m4s",
        "content": "The exact transcribed text for that segment."
    }

    If the audio has only one speaker, use Speaker 1 throughout. Ensure the transcript is complete but concise, covering the entire audio without duplicates.
    '''

    # Tạo audio part từ bytes
    mime_type = f"audio/{file_extension}"
    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            prompt,
            audio_part
        ],
        config=types.GenerateContentConfig(
            temperature=0,
            top_p=0,
            response_mime_type='application/json',
            response_schema={
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "speaker": {"type": "string", "description": "Speaker label, e.g., Speaker 1"},
                        "timestamp": {"type": "string", "description": "Estimated timestamp range like 0h0m0s-0h1m4s"},
                        "content": {"type": "string", "description": "Verbatim transcribed text for the segment"}
                    },
                    "required": ["speaker", "timestamp", "content"]
                }
            },
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )

    return response.text
