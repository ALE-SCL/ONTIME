import os
from pathlib import Path
from typing import Dict, Optional
from elevenlabs.client import ElevenLabs
from src.utils.security import get_api_key
from src.utils.helpers import generate_hash

# Configuración extendida de voces
AVAILABLE_VOICES: Dict[str, Dict] = {
    "Fernando_P": {
        "id": "X154G7FAoyNV4grCKAe1",
        "key_identifier": "Fernando_P"
    },
    "RICARDO_1": {
        "id": "KqOWeICsh4ncqaTQlehb",
        "key_identifier": "RICARDO_1"
    },
    "RICARDO_2": {
        "id": "PrvSOldH32de0Ovbqmaz",
        "key_identifier": "RICARDO_2"
    },
    "MILENA_1": {
        "id": "chqjP7q1s4cuHUFJ3CHv",
        "key_identifier": "MILENA_1"
    },
    "MILENA_2": {
        "id": "Wtl9vUInpKWLp0jtGnxi",
        "key_identifier": "MILENA_2"
    }
}

class ElevenLabsClient:
    def __init__(self):
        """Inicializa los directorios de salida."""
        self.drafts_dir = Path("output_audio/drafts")
        self.drafts_dir.mkdir(parents=True, exist_ok=True)
        # Diccionario para almacenar clientes por llave para evitar re-instanciar
        self._clients_cache: Dict[str, ElevenLabs] = {}

    def _get_client_for_voice(self, voice_name: str) -> ElevenLabs:
        """Obtiene el cliente adecuado para la voz seleccionada."""
        key_id = AVAILABLE_VOICES[voice_name]["key_identifier"]
        
        if key_id not in self._clients_cache:
            api_key = get_api_key(key_id)
            if not api_key:
                # Si no hay llave específica, intentar con la default o la de Fernando_P
                api_key = get_api_key("Fernando_P")
                if not api_key:
                    raise ValueError(f"No se encontró ninguna API Key para la voz {voice_name}.")
            
            self._clients_cache[key_id] = ElevenLabs(api_key=api_key)
        
        return self._clients_cache[key_id]

    def generate_speech(self, text: str, voice_name: str = "Fernando_P") -> Path:
        """Genera audio con soporte para múltiples llaves."""
        if voice_name not in AVAILABLE_VOICES:
            raise ValueError(f"La voz '{voice_name}' no está configurada.")
        
        voice_info = AVAILABLE_VOICES[voice_name]
        voice_id = voice_info["id"]
        
        # Generar nombre de archivo único
        text_hash = generate_hash(f"{text}_{voice_id}")
        output_path = self.drafts_dir / f"{text_hash}.mp3"
        
        if output_path.exists():
            print(f"Audio cargado desde caché: {output_path}")
            return output_path

        # Si es un ID de prueba (placeholder), lanzar error explicativo
        if "PLACEHOLDER" in voice_id:
            raise ValueError(f"La voz {voice_name} es un placeholder. Necesitas configurar un Voice ID real.")

        print(f"Generando audio (Voz: {voice_name})...")
        
        try:
            client = self._get_client_for_voice(voice_name)
            audio_generator = client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            
            audio_data = b"".join(list(audio_generator))
            with open(output_path, "wb") as f:
                f.write(audio_data)
                
            return output_path
            
        except Exception as e:
            print(f"Error en ElevenLabs ({voice_name}): {e}")
            raise
