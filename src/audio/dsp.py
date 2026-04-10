import os
from pathlib import Path
import numpy as np
import soundfile as sf
from pedalboard import (
    Pedalboard, 
    HighpassFilter, 
    Compressor, 
    PeakFilter, 
    Gain, 
    Reverb,
    Distortion
)
from pedalboard.io import AudioFile

class AudioProcessor:
    def __init__(self):
        """Inicializa la cadena de efectos (Pedalboard)."""
        self.output_dir = Path("output_audio/processed")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuración de la cadena de masterización profesional
        self.board = Pedalboard([
            # 1. Limpieza de graves (HPF)
            HighpassFilter(cutoff_frequency_hz=100),
            
            # 2. EQ Creativa: Cuerpo
            PeakFilter(cutoff_frequency_hz=300, gain_db=2.0, q=1.0),
            
            # 3. EQ Creativa: Claridad/Brillo
            PeakFilter(cutoff_frequency_hz=5000, gain_db=1.5, q=1.0),
            
            # 4. Compresión Radial (4:1)
            Compressor(threshold_db=-15, ratio=4),
            
            # 5. Saturación sutil (Cinta)
            Distortion(drive_db=2), # Emulación de saturación
            
            # 6. Reverb Room (Sutil)
            Reverb(room_size=0.1, dry_level=0.98, wet_level=0.02),
            
            # 7. Ganancia final / Normalización a -6dB
            Gain(gain_db=0)
        ])

    def process_voice(self, input_path: Path) -> Path:
        """
        Aplica la cadena de masterización a un archivo de audio.
        """
        output_path = self.output_dir / f"proc_{input_path.stem}.wav"
        
        print(f"Masterizando audio: {input_path.name}...")
        
        with AudioFile(str(input_path)) as f:
            audio = f.read(f.frames)
            samplerate = f.samplerate
        
        # Aplicar la cadena de efectos
        processed_audio = self.board(audio, samplerate)
        
        # Normalización a -3 dB (Pico Máximo)
        max_val = np.max(np.abs(processed_audio))
        if max_val > 0:
            target_peak = 10 ** (-3 / 20)
            normalization_gain = target_peak / max_val
            processed_audio *= normalization_gain

        # Guardar el resultado en WAV
        sf.write(str(output_path), processed_audio.T, samplerate)
        
        print(f"Audio masterizado con éxito: {output_path}")
        return output_path

if __name__ == "__main__":
    drafts = list(Path("output_audio/drafts").glob("*.mp3"))
    if drafts:
        processor = AudioProcessor()
        try:
            processed_file = processor.process_voice(drafts[0])
            print(f"Prueba DSP exitosa: {processed_file}")
        except Exception as e:
            print(f"Error en prueba DSP: {e}")
    else:
        print("No hay archivos en 'output_audio/drafts' para probar el DSP.")
