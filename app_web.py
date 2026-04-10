import streamlit as st
from datetime import datetime
from pathlib import Path
from src.audio.api_client import ElevenLabsClient, AVAILABLE_VOICES
from src.audio.dsp import AudioProcessor
from src.audio.mixer import AudioMixer

# Configuración de Página
st.set_page_config(page_title="ON TIME - Radio Automation", page_icon="🎙️")

st.title("🎙️ ON TIME - Radio Automation")
st.markdown("Sistema profesional de locución radial con post-producción automática.")

# Inicializar clientes
@st.cache_resource
def init_clients():
    return ElevenLabsClient(), AudioProcessor(), AudioMixer()

api_client, audio_processor, audio_mixer = init_clients()

# UI: Selección de Voz y Texto
voice_name = st.selectbox("Elige la Voz:", options=list(AVAILABLE_VOICES.keys()))
text_input = st.text_area("Texto de la Locución:", height=200, placeholder="Escribe aquí el texto que deseas locutar...")

if st.button("GENERAR PRODUCCIÓN FINAL"):
    if not text_input.strip():
        st.warning("⚠️ Por favor ingresa algún texto.")
    elif not api_client:
        st.error("❌ El sistema no está configurado.")
    else:
        try:
            with st.status("Procesando producción...", expanded=True) as status:
                # 1. Generación
                st.write(f"🛰️ Generando voz con {voice_name}...")
                raw_path = api_client.generate_speech(text_input, voice_name)
                
                # 2. Masterización
                st.write("🎚️ Masterizando Voz (EQ, Compresión)...")
                processed_voice_path = audio_processor.process_voice(raw_path)
                
                # 3. Preparar Nombre de Archivo Profesional
                timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                nice_name = f"ON_TIME_FINAL_{voice_name}_{timestamp}.mp3"
                
                # 4. Mezcla Final
                st.write("🎵 Realizando Mezcla con Cama y Outro (Auto-Ducking)...")
                final_path = audio_mixer.create_final_mix(processed_voice_path, voice_name, custom_filename=nice_name)
                
                status.update(label="✅ ¡Producción Lista!", state="complete", expanded=False)

            st.success(f"Archivo generado: {final_path.name}")
            st.audio(str(final_path), format="audio/mpeg")

            with open(final_path, "rb") as f:
                st.download_button(
                    label="⬇️ Descargar Producción Final (MP3)",
                    data=f,
                    file_name=final_path.name,
                    mime="audio/mpeg"
                )

        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("ON TIME - Sistema de Producción de Radio Profesional")
