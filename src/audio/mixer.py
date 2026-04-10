import os
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

class AudioMixer:
    def __init__(self):
        self.base_media_path = Path("Media_ON_TIME")
        self.output_dir = Path("output_audio/final")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Niveles Profesionales
        self.MUSIC_DUCKED = -15.0   # Nivel con locución
        self.MUSIC_BRIDGE = 0    # Nivel sin locución
        self.FINAL_NORM = 0      # Nivel final
        self.FADE_TIME = 400        # Tiempo de fundido (ms)

    def _get_assets_for_voice(self, voice_name: str):
        if "Ricardo" in voice_name:
            folder = self.base_media_path / "RICARDO"
            cama = folder / "CAMA BASE RICARDO.mp3"
            outro = folder / "OUTRO BASE RICARDO.mp3"
        else:
            folder = self.base_media_path / "FERNANDO_P"
            cama = folder / "CAMA BASE MILENA.mp3"
            outro = folder / "OUTRO BASE MILENA.mp3"
        return cama, outro

    def create_final_mix(self, voice_path: Path, voice_name: str, custom_filename: str = None) -> Path:
        print(f"Mezclando producción final con técnica de remate anticipado para {voice_name}...")
        
        voice = AudioSegment.from_file(voice_path)
        cama_path, outro_path = self._get_assets_for_voice(voice_name)
        cama_original = AudioSegment.from_file(cama_path)
        outro = AudioSegment.from_file(outro_path)

        # 1. Detectar el final real de la voz
        ranges = detect_nonsilent(voice, min_silence_len=800, silence_thresh=-40)
        last_voice_end = ranges[-1][1] if ranges else len(voice)

        # 2. Punto de Transición: 600ms después de que termine la voz
        transition_point = last_voice_end + 600

        # 3. Preparar la cama musical solo hasta el punto de transición
        music_track = cama_original
        while len(music_track) < transition_point:
            music_track += cama_original
        music_track = music_track[:transition_point]

        # 4. Aplicar Ducking a la cama (para que la voz se entienda)
        music_bridge = music_track.normalize(headroom=abs(self.MUSIC_BRIDGE))
        music_ducked = music_track.normalize(headroom=abs(self.MUSIC_DUCKED))
        
        final_music_cama = music_bridge
        for start, end in ranges:
            # Aseguramos que los rangos no excedan el punto de transición
            s = min(start, transition_point)
            e = min(end, transition_point)
            
            if s >= e: continue

            d_start = max(0, s - 200)
            d_mid = min(len(final_music_cama), s + 200)
            u_start = e
            u_end = min(len(final_music_cama), e + self.FADE_TIME)
            
            if d_mid > d_start:
                dur = d_mid - d_start
                trans_down = music_bridge[d_start:d_mid].fade_out(dur).overlay(music_ducked[d_start:d_mid].fade_in(dur))
                final_music_cama = final_music_cama[:d_start] + trans_down + final_music_cama[d_mid:]
            
            if u_start > d_mid:
                final_music_cama = final_music_cama[:d_mid] + music_ducked[d_mid:u_start] + final_music_cama[u_start:]
                
            if u_end > u_start:
                dur = u_end - u_start
                trans_up = music_ducked[u_start:u_end].fade_out(dur).overlay(music_bridge[u_start:u_end].fade_in(dur))
                final_music_cama = final_music_cama[:u_start] + trans_up + final_music_cama[u_end:]

        # 5. FUNDIR CON EL OUTRO (Fade in mediante crossfade de 200ms)
        # El remate comienza exactamente 600ms después del fin de la voz.
        outro_norm = outro.normalize(headroom=abs(self.MUSIC_BRIDGE))
        full_music_track = final_music_cama.append(outro_norm, crossfade=200)

        # 6. Mezcla Final: Superponemos la voz sobre esta nueva pista musical
        final_audio = full_music_track.overlay(voice)

        # 7. Normalización Final a -3 dB
        final_audio = final_audio.normalize(headroom=abs(self.FINAL_NORM))

        # 8. Exportar
        output_name = custom_filename if custom_filename else f"PROD_FINAL_{voice_path.stem}.mp3"
        output_path = self.output_dir / output_name
        final_audio.export(output_path, format="mp3", bitrate="128k")
        
        return output_path
