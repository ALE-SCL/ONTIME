import hashlib
import pathlib
from datetime import datetime

def generate_hash(text_to_hash: str) -> str:
    """
    Genera un hash SHA-256 para una cadena de texto dada.
    
    Args:
        text_to_hash: El texto para el cual generar el hash.
        
    Returns:
        El hash SHA-256 en formato hexadecimal.
    """
    return hashlib.sha256(text_to_hash.encode('utf-8')).hexdigest()

def generate_timestamped_filename(prefix: str = "Radio_Nota", extension: str = "wav") -> str:
    """
    Genera un nombre de archivo con un timestamp actual.
    Ejemplo: Radio_Nota_20251226_143005.wav
    
    Args:
        prefix: El prefijo del nombre de archivo.
        extension: La extensión del archivo, sin el punto.
        
    Returns:
        El nombre de archivo formateado.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def get_downloads_folder() -> pathlib.Path:
    """
    Obtiene la ruta a la carpeta de Descargas del usuario de forma multiplataforma.
    
    Returns:
        Un objeto Path apuntando a la carpeta de Descargas.
    """
    return pathlib.Path.home() / "Downloads"

# Ejemplo de uso (se puede eliminar más tarde)
if __name__ == '__main__':
    texto = "Esta es una prueba de locución."
    hashed_text = generate_hash(texto)
    print(f"Texto: '{texto}'")
    print(f"Hash: {hashed_text}")
    
    filename = generate_timestamped_filename()
    print(f"Nombre de archivo generado: {filename}")
    
    downloads_path = get_downloads_folder()
    print(f"La carpeta de descargas es: {downloads_path}")
    
    # Simular la creación de un archivo de destino
    final_path = downloads_path / filename
    print(f"La ruta final del archivo sería: {final_path}")
