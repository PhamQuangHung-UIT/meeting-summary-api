import os
import sys
import mimetypes
import tempfile
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError('GEMINI_API_KEY is not set in .env file')

genai.configure(api_key=GEMINI_API_KEY)

def transcribe_gemini(audio_bytes: bytes, file_extension: str):
    prompt = '''
    transcript audio sau, nghe được người nói nào nói thì đánh Speaker 1, Speaker 2,..., đánh thời gian câu nói trong audio, lưu ý chỉ xuất ra duy nhất json không xuất gì khác, ví dụ:
    [
        {
            "speaker": "Speaker ...",
            "timestamp": "0h0m0s-0h1m4s",
            "content": "abcdef"
        },
        {
            "speaker": "Speaker ...",
            "timestamp": "0h0m0s-0h1m4s",
            "content": "abcdef"
        },
        ...
    ]
    '''
    temp_file_path = None
    try:
        # Tạo một file tạm thời để ghi dữ liệu audio bytes
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_file_path = temp_audio_file.name
        
        print(f'Uploading audio file from temporary path: {temp_file_path}...')
        
        # Xác định loại MIME
        mime_type, _ = mimetypes.guess_type(temp_file_path)
        if mime_type is None:
            raise ValueError(f"Could not determine MIME type for file with extension .{file_extension}")

        uploaded_file = genai.upload_file(path=temp_file_path, display_name=f"audio_upload.{file_extension}")
        print(f'Successfully uploaded file {uploaded_file.display_name} as: {uploaded_file.uri}')

        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash-lite',
            generation_config={
                'temperature': 0,
                'top_p': 0
            }
        )
        
        print('Sending prompt to Gemini...')

        response = model.generate_content(
            contents=[{
                'role': 'user',
                'parts': [
                    {'text': prompt},  # nội dung prompt
                    uploaded_file
                ]
            }],
            stream=True
        )
        
        full_response_content = ""
        for chunk in response:
            if chunk.text:
                full_response_content += chunk.text
        
        print('\nCompleted')

        return full_response_content

    except Exception as error:
        print(f'Error sending prompt to Gemini: {error}')
        raise error
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Temporary file {temp_file_path} deleted.")


