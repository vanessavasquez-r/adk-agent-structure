from dotenv import load_dotenv
import os

load_dotenv()

abspath = os.path.abspath(os.path.dirname(__file__))

BUCKET_NAME="test_rfp_agent"
PROJECT_ID="prueba-transcripciones-speech"
LOCATION="us-central1"
MODEL="gemini-2.5-flash"