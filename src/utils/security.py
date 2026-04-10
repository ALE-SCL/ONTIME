import keyring
import keyring.errors
import streamlit as st
from typing import Optional

# Nombre de servicio único para la aplicación
SERVICE_NAME = "ON_TIME_Radio_App"

def save_api_key(api_key: str, key_name: str = "default") -> bool:
    """
    Guarda una API Key de ElevenLabs de forma segura (Solo local).
    """
    try:
        identifier = f"elevenlabs_api_key_{key_name}"
        keyring.set_password(SERVICE_NAME, identifier, api_key)
        print(f"API Key '{key_name}' guardada de forma segura localmente.")
        return True
    except Exception as e:
        print(f"Error al guardar la clave local {key_name}: {e}")
        return False

def get_api_key(key_name: str = "default") -> Optional[str]:
    """
    Obtiene una API Key específica. 
    Primero intenta desde Streamlit Secrets (Nube) y luego desde Keyring (Local).
    """
    # 1. Intentar desde Streamlit Secrets (Nube / Local .streamlit/secrets.toml)
    try:
        secret_key = f"ELEVENLABS_API_KEY_{key_name.upper()}"
        if secret_key in st.secrets:
            return st.secrets[secret_key]
        
        # Intentar con la genérica
        if "ELEVENLABS_API_KEY" in st.secrets:
            return st.secrets["ELEVENLABS_API_KEY"]
    except:
        pass

    # 2. Intentar desde Keyring (Local)
    try:
        identifier = f"elevenlabs_api_key_{key_name}"
        return keyring.get_password(SERVICE_NAME, identifier)
    except Exception as e:
        print(f"Error al obtener la clave {key_name} desde keyring: {e}")
        return None
