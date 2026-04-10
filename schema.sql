-- Estructura para SQLite
CREATE TABLE IF NOT EXISTS locuciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    texto_hash TEXT NOT NULL,
    texto_original TEXT NOT NULL,
    ganancia_db REAL DEFAULT 0.0,
    ruta_archivo_final TEXT,
    estado TEXT DEFAULT 'completado'
);

CREATE INDEX IF NOT EXISTS idx_hash ON locuciones (texto_hash);
