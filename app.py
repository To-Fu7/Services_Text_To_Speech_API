from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import subprocess
from g2p_id import G2P
import os                                                                           
import tempfile

app = FastAPI(
    title="TTS Language Converter API",
    description="API Konversi Text To Speech (Indonesia & Inggris)",
    version="1.2.0"
)

g2p = G2P()

class TTSRequest(BaseModel):
    text: str
    lang: str = "eng"


@app.post("/tts", response_class=FileResponse)
def generate_tts(request: TTSRequest):
    """
    Generate speech audio from text and return it as a WAV file.
    Each request gets a unique timestamped filename (e.g., outputs_2025-11-12_143500.wav)
    that exists only temporarily inside the container.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    temp_dir = tempfile.gettempdir()
    output_filename = f"outputs_{timestamp}.wav"
    output_path = os.path.join(temp_dir, output_filename)

    TEXT = request.text
    CHOOSEN_LANGUAGE = request.lang.lower()

    if CHOOSEN_LANGUAGE != "eng":
        CONFIG = "./configs/config.json"
        VOICE = "wibowo"
        PATH = "./models/model_indo.pth"
        CONVERTED_TEXT = g2p(TEXT)
        print(f"lang = indo → generating {output_filename}")
        subprocess.run([
            "tts",
            "--text", CONVERTED_TEXT,
            "--model_path", PATH,
            "--config_path", CONFIG,
            "--speaker_idx", VOICE,
            "--out_path", output_path
        ], check=True)
    else:
        print(f"lang = eng → generating {output_filename}")
        subprocess.run([
            "tts",
            "--text", TEXT,
            "--out_path", output_path
        ], check=True)

    if os.path.exists(output_path):
        return FileResponse(
            path=output_path,
            media_type="audio/wav",
            filename=output_filename 
        )
    else:
        raise HTTPException(status_code=500, detail="TTS generation failed.")
