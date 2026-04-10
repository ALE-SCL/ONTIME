import keyring
import keyring.errors
from typing import Optional

# Nombre de servicio único para la aplicación
SERVICE_NAME = "ON_TIME_Radio_App"

def save_api_key(api_key: str, key_name: str = "default") -> bool:
    """
    Guarda una API Key de ElevenLabs de forma segura.
    key_name permite diferenciar entre llaves de distintos locutores si fuera necesario.
    """
    try:
        identifier = f"elevenlabs_api_key_{key_name}"
        keyring.set_password(SERVICE_NAME, identifier, api_key)
        print(f"API Key '{key_name}' guardada de forma segura.")
        return True
    except Exception as e:
        print(f"Error al guardar la clave {key_name}: {e}")
        return False

def get_api_key(key_name: str = "default") -> Optional[str]:
    """Obtiene una API Key específica desde el sistema."""
    try:
        identifier = f"elevenlabs_api_key_{key_name}"
        return keyring.get_password(SERVICE_NAME, identifier)
    except Exception as e:
        print(f"Error al obtener la clave {key_name}: {e}")
        return None
