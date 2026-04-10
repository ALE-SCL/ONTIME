# SAR v2.0 (Radio Automation)

Sistema profesional de automatización de locución radial con post-producción automática basado en **Streamlit**. Diseñado para correr en cualquier navegador local en macOS y Windows sin dependencias gráficas pesadas.

## 1. Características Principales

- **Interfaz Web Local:** Basada en Streamlit (rápida, estable y multiplataforma).
- **Core:** Python 3.9+.
- **Motor de Voz:** ElevenLabs API v1.x (Multilingüe v2).
- **Masterización Radial (DSP):** Pedalboard (Spotify) + Soundfile.
- **Normalización Automática:** Pico máximo a -6dB.

## 2. Instalación y Uso

### Configuración del Entorno
1.  **Entorno Virtual:** `python3 -m venv .venv`
2.  **Activar Entorno:** `source .venv/bin/activate` (macOS) o `.venv\Scripts\activate` (Windows).
3.  **Instalar Dependencias:** `pip install -r requirements.txt`

### Ejecución de la Aplicación
Para lanzar el sistema, usa este comando desde la raíz del proyecto:
```bash
streamlit run app_web.py
```

## 3. Flujo de Trabajo
1.  **Entrada:** Escribe o pega el texto en el editor de la web.
2.  **Voz:** Elige entre las voces configuradas (Fernando_P).
3.  **Procesamiento:** El sistema descarga la voz y le aplica EQ, Compresión y Saturación.
4.  **Descarga:** Escucha el resultado en el navegador y descárgalo con un clic.

## 4. Directorios del Proyecto
- `src/audio/`: Lógica de API ElevenLabs y Procesamiento DSP.
- `src/utils/`: Seguridad (keyring), Base de Datos (SQLite) y Utilidades.
- `output_audio/`: Audios generados (crudos y masterizados).
- `Media_SAR/`: Recursos de audio (camas, intros, etc).
