import sqlite3
import pathlib
from typing import Optional, Dict

# Definir la ruta a la base de datos
DB_NAME = "radio_database.sqlite"
DB_PATH = pathlib.Path(__file__).parent.parent.parent / "database" / DB_NAME
SCHEMA_PATH = pathlib.Path(__file__).parent.parent.parent / "schema.sql"

def get_db_connection() -> sqlite3.Connection:
    """Establece y devuelve una conexión a la base de datos."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos."""
    try:
        with get_db_connection() as conn:
            with open(SCHEMA_PATH, 'r') as f:
                conn.executescript(f.read())
            print("Base de datos inicializada correctamente.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")

def add_locucion(texto_hash: str, texto_original: str, ganancia_db: float, ruta_archivo: str) -> Optional[int]:
    """Añade un registro de locución."""
    sql = "INSERT INTO locuciones (texto_hash, texto_original, ganancia_db, ruta_archivo_final) VALUES (?, ?, ?, ?)"
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (texto_hash, texto_original, ganancia_db, ruta_archivo))
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"Error al añadir locución: {e}")
        return None

def find_locucion_by_hash(texto_hash: str) -> Optional[Dict]:
    """Busca una locución por su hash."""
    sql = "SELECT * FROM locuciones WHERE texto_hash = ?"
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (texto_hash,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except Exception as e:
        print(f"Error al buscar locución: {e}")
        return None
