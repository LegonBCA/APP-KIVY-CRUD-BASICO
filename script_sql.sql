-- Script SQL para la base de datos de la App To-Do
-- Base de datos: SQLite3
-- Tabla: tareas

-- Crear tabla de tareas
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    completada INTEGER DEFAULT 0,
    fecha_creacion TEXT NOT NULL,
    fecha_actualizacion TEXT
);

-- Insertar datos de ejemplo
INSERT INTO tareas (titulo, descripcion, completada, fecha_creacion, fecha_actualizacion) VALUES
('Estudiar Python', 'Completar el curso de Python básico', 0, '2024-01-15 10:30:00', '2024-01-15 10:30:00'),
('Hacer ejercicio', 'Correr 30 minutos', 0, '2024-01-15 10:30:00', '2024-01-15 10:30:00'),
('Comprar comida', 'Ir al supermercado', 0, '2024-01-15 10:30:00', '2024-01-15 10:30:00');

-- Consultas útiles para verificar los datos

-- Ver todas las tareas
SELECT * FROM tareas;

-- Ver solo tareas pendientes
SELECT * FROM tareas WHERE completada = 0;

-- Ver solo tareas completadas
SELECT * FROM tareas WHERE completada = 1;

-- Contar total de tareas
SELECT COUNT(*) as total_tareas FROM tareas;

-- Contar tareas completadas
SELECT COUNT(*) as tareas_completadas FROM tareas WHERE completada = 1;

-- Contar tareas pendientes
SELECT COUNT(*) as tareas_pendientes FROM tareas WHERE completada = 0;

-- Ver estadísticas generales
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN completada = 1 THEN 1 ELSE 0 END) as completadas,
    SUM(CASE WHEN completada = 0 THEN 1 ELSE 0 END) as pendientes
FROM tareas;
