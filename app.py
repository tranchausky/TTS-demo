import html
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

app = FastAPI()

DEFAULT_ENGINE = "piper"
DEFAULT_MODEL = "en"

PIPER_MODELS = {
    "en": "/voices/en_US-lessac-high/en_US-lessac-high.onnx",
    "en_us": "/voices/en_US-lessac-high/en_US-lessac-high.onnx",
    "english": "/voices/en_US-lessac-medium/en_US-lessac-medium.onnx",
    "amy": "/voices/en_US-amy-medium/en_US-amy-medium.onnx",
    "vi": "/voices/vi_VN-vais1000-medium/vi_VN-vais1000-medium.onnx",
    "vietnamese": "/voices/vi_VN-vais1000-medium/vi_VN-vais1000-medium.onnx",
}


class TTSRequest(BaseModel):
    text: str
    engine: Optional[str] = None  # piper | supertonic
    model: Optional[str] = None
    voice: Optional[str] = None
    language: Optional[str] = None  # en | vi | ko | ...


@app.get("/health")
def health():
    return {
        "status": "ok",
        "default_engine": DEFAULT_ENGINE,
        "default_model": DEFAULT_MODEL,
        "piper_models": list(PIPER_MODELS.keys()),
        "engines": ["piper", "supertonic"],
    }


@app.get("/", response_class=Response)
def index():
    page = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>TTS Test</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 820px;
      margin: 40px auto;
      padding: 0 16px;
      line-height: 1.5;
    }
    label {
      display: block;
      margin-top: 14px;
      font-weight: bold;
    }
    textarea, select, input, button {
      width: 100%;
      box-sizing: border-box;
      font-size: 16px;
      margin-top: 8px;
    }
    textarea {
      min-height: 140px;
      padding: 12px;
    }
    select, input {
      padding: 10px;
    }
    button {
      padding: 12px;
      cursor: pointer;
      margin-top: 18px;
    }
    audio {
      width: 100%;
      margin-top: 20px;
    }
    pre {
      background: #f4f4f4;
      padding: 12px;
      overflow: auto;
      border-radius: 6px;
    }
    .status {
      margin-top: 12px;
      font-weight: bold;
    }
    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }
    @media (max-width: 640px) {
      .row {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <h1>TTS Test</h1>

    <div class="row">
      <div>
        <label>Engine</label>
        <select id="engine" onchange="renderModelOptions()">
          <option value="piper">piper</option>
          <option value="supertonic">supertonic</option>
        </select>
      </div>

      <div>
        <label>Model / Language</label>
        <select id="model"></select>
      </div>
    </div>

    <div id="supertonicVoiceBox" style="display:none;">
      <label>Supertonic Voice</label>
      <select id="supertonicVoice"></select>
    </div>

  <label>Text</label>
  <textarea id="text">Hello, this is a text to speech test.</textarea>

  <button onclick="generate()">Generate & Play</button>

  <div class="status" id="status"></div>
  <audio id="audio" controls></audio>

  <h3>Available engines/models</h3>
  <pre id="modelsJson">Loading...</pre>

  <script>
    let modelsData = null;

    async function loadModels() {
      const res = await fetch('/models');
      modelsData = await res.json();
      document.getElementById('modelsJson').textContent = JSON.stringify(modelsData, null, 2);
      renderModelOptions();
    }

    function renderModelOptions() {
      const engine = document.getElementById('engine').value;
      const modelSelect = document.getElementById('model');
      const voiceBox = document.getElementById('supertonicVoiceBox');
      const voiceSelect = document.getElementById('supertonicVoice');

      modelSelect.innerHTML = '';
      voiceSelect.innerHTML = '';

      if (!modelsData || !modelsData.engines) {
        return;
      }

      if (engine === 'piper') {
        voiceBox.style.display = 'none';

        const piperModels = modelsData.engines.piper || {};
        Object.keys(piperModels).forEach((key) => {
          const opt = document.createElement('option');
          opt.value = key;
          opt.textContent = key;
          modelSelect.appendChild(opt);
        });
      }

      if (engine === 'supertonic') {
        voiceBox.style.display = 'block';

        const langs = (modelsData.engines.supertonic && modelsData.engines.supertonic.languages) || ['en', 'vi'];
        langs.forEach((key) => {
          const opt = document.createElement('option');
          opt.value = key;
          opt.textContent = key;
          modelSelect.appendChild(opt);
        });

        const voices = (modelsData.engines.supertonic && modelsData.engines.supertonic.voices) || ['F1', 'F2', 'F3', 'F4', 'F5', 'M1', 'M2', 'M3', 'M4', 'M5'];
        voices.forEach((key) => {
          const opt = document.createElement('option');
          opt.value = key;
          opt.textContent = key;
          if (key === 'F1') opt.selected = true;
          voiceSelect.appendChild(opt);
        });
      }
    }

   async function generate() {
      const status = document.getElementById('status');
      const audio = document.getElementById('audio');

      const engine = document.getElementById('engine').value;
      const model = document.getElementById('model').value;
      const supertonicVoice = document.getElementById('supertonicVoice').value;
      const text = document.getElementById('text').value;

      status.textContent = 'Generating...';
      audio.removeAttribute('src');

      let payload = { text, engine };

      if (engine === 'piper') {
        payload.model = model;
      }

      if (engine === 'supertonic') {
        payload.language = model;
        payload.voice = supertonicVoice;
      }

      try {
        const res = await fetch('/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (!res.ok) {
          const errText = await res.text();
          throw new Error(errText);
        }

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);

        audio.src = url;
        await audio.play();

        status.textContent = 'Done';
      } catch (err) {
        status.textContent = 'Error: ' + err.message;
      }
    }

    loadModels();
  </script>
</body>
</html>
"""
    return Response(content=page, media_type="text/html")

@app.get("/models")
def list_models():
    return {
        "default_engine": DEFAULT_ENGINE,
        "default_model": DEFAULT_MODEL,
        "engines": {
            "piper": PIPER_MODELS,
            "supertonic": {
                "note": "Uses installed supertonic CLI/Python package",
                "languages": ["en", "vi"],
                "voices": ["F1", "F2", "F3", "F4", "F5", "M1", "M2", "M3", "M4", "M5"],
            },
        },
    }


def run_piper(text: str, model_key: str) -> bytes:
    model_path = PIPER_MODELS.get(model_key)
    if not model_path:
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Unknown Piper model: {model_key}",
                "available_models": list(PIPER_MODELS.keys()),
            },
        )

    if not Path(model_path).is_file():
        raise HTTPException(
            status_code=500,
            detail=f"Piper model file not found: {model_path}",
        )

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        out_path = f.name

    try:
        subprocess.run(
            ["piper", "--model", model_path, "--output_file", out_path],
            input=text.encode("utf-8"),
            check=True,
        )
        return Path(out_path).read_bytes()
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Piper failed with exit code {e.returncode}",
        )
    finally:
        Path(out_path).unlink(missing_ok=True)


def run_supertonic(text: str, language: str, voice: str = "F1") -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        out_path = f.name

    try:
        subprocess.run(
            [
                "supertonic",
                "tts",
                text,
                "-o",
                out_path,
                "--voice",
                voice,
                "--lang",
                language,
                "--steps",
                "8",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        return Path(out_path).read_bytes()

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="supertonic command not found. Did you install `pip install supertonic`?",
        )

    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Supertonic failed",
                "returncode": e.returncode,
                "stderr": e.stderr,
                "stdout": e.stdout,
            },
        )

    finally:
        Path(out_path).unlink(missing_ok=True)


@app.post("/tts")
def tts(req: TTSRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    engine = (req.engine or DEFAULT_ENGINE).strip().lower()

    if engine == "piper":
        model_key = req.voice or req.model or DEFAULT_MODEL
        model_key = model_key.strip().lower()
        audio = run_piper(text, model_key)
        return Response(content=audio, media_type="audio/wav")

    if engine == "supertonic":
        language = (req.language or req.model or "en").strip().lower()
        voice = (req.voice or "F1").strip().upper()

        allowed_voices = {"F1", "F2", "F3", "F4", "F5", "M1", "M2", "M3", "M4", "M5"}
        if voice not in allowed_voices:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Unknown Supertonic voice: {voice}",
                    "available_voices": sorted(allowed_voices),
                },
            )

        audio = run_supertonic(text, language, voice)
        return Response(content=audio, media_type="audio/wav")

    raise HTTPException(
        status_code=400,
        detail={
            "error": f"Unknown engine: {engine}",
            "available_engines": ["piper", "supertonic"],
        },
    )