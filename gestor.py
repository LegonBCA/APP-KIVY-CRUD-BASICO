#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Base de Datos SQLite para App To-Do
Maneja todas las operaciones CRUD de las tareas
"""

import sqlite3
import os
from datetime import datetime


class GestorTareas:
    """
    Clase para gestionar las tareas en la base de datos SQLite
    """
    
    def __init__(self, nombre_db="tareas.db"):
        """
        Inicializa el gestor de base de datos
        
        Args:
            nombre_db (str): Nombre del archivo de base de datos
        """
        self.nombre_db = nombre_db
        self.inicializar_db()
    
    def inicializar_db(self):
        """
        Crea la tabla de tareas si no existe
        """
        try:
            with sqlite3.connect(self.nombre_db) as conexion:
                cursor = conexion.cursor()
                
                # Crear tabla de tareas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tareas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        descripcion TEXT,
                        completada INTEGER DEFAULT 0,
                        fecha_creacion TEXT NOT NULL,
                        fecha_actualizacion TEXT
                    )
                ''')
                
                conexion.commit()
                print("✅ Base de datos inicializada correctamente")
                
        except sqlite3.Error as e:
            print(f"❌ Error al inicializar la base de datos: {e}")
    
    def agregar_tarea(self, titulo, descripcion=""):
        """
        Agrega una nueva tarea a la base de datos
        
        Args:
            titulo (str): Título de la tarea
            descripcion (str): Descripción de la tarea
            
        Returns:
            bool: True si se agregó correctamente, False en caso contrario
        """
        try:
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with sqlite3.connect(self.nombre_db) as conexion:
                cursor = conexion.cursor()
                
                cursor.execute('''
                    INSERT INTO tareas (titulo, descripcion, fecha_creacion, fecha_actualizacion)
                    VALUES (?, ?, ?, ?)
                ''', (titulo, descripcion, fecha_actual, fecha_actual))
                
                conexion.commit()
                print(f"✅ Tarea '{titulo}' agregada correctamente")
                return True
                
        except sqlite3.Error as e:
            print(f"❌ Error al agregar tarea: {e}")
            return False
    
    def obtener_todas_tareas(self):
        """
        Obtiene todas las tareas de la base de datos
        
        Returns:
            list: Lista de tuplas con los datos de las tareas
        """
        try:
            with sqlite3.connect(self.nombre_db) as conexion:
                cursor = conexion.cursor()
                
                cursor.execute('''
                    SELECT id, titulo, descripcion, completada, fecha_creacion, fecha_actualizacion
                    FROM tareas
                    ORDER BY fecha_creacion DESC
                ''')
                
                tareas = cursor.fetchall()
                return tareas
                
        except sqlite3.Error as e:
            print(f"❌ Error al obtener tareas: {e}")
            return []
    
    def obtener_tarea_por_id(self, tarea_id):
        """
        Obtiene una tarea específica por su ID
        
        Args:
            tarea_id (int): ID de la tarea
            
        Returns:
            tuple: Datos de la tarea o None si no existe
        """
        try:
            with sqlite3.connect(self.nombre_db) as conexion:
                cursor = conexion.cursor()
                
                cursor.execute('''
                    SELECT id, titulo, descripcion, completada, fecha_creacion, fecha_actualizacion
                    FROM tareas
                    WHERE id = ?
                ''', (tarea_id,))
                
                tarea = cursor.fetchone()
                return tarea
                
        except sqlite3.Error as e:
            print(f"❌ Error al obtener tarea: {e}")
            return None
    
    def actualizar_tarea(self, tarea_id, titulo, descripcion="", completada=False):
        """
        Actualiza una tarea existente
        
        Args:
            tarea_id (int): ID de la tarea
            titulo (str): Nuevo título
            descripcion (str): Nueva descripción
            completada (bool): Estado de completada
            
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            estado_completada = 1 if completada else 0
            
            with sqlite3.connect(self.nombre_db) as conexion:
                cursor = conexion.cursor()
                
                cursor.execute('''
                    UPDATE tareas
                    SET titulo = ?, descripcion = ?, completada = ?, fecha_actualizacion = ?
                    WHERE id = ?
                ''', (titulo, descripcion, estado_completada, fecha_actual, tarea_id))
                
                if cursor.rowcount > 0:
                    conexion.commit()
                    print(f"✅ Tarea ID {tarea_id} actualizada correctamente")
                    return True
                else:
                    print(f"⚠️ No se encontró la tarea con ID {tarea_id}")
                    return False
                    
        except sqlite3.Error as e:
            print(f"❌ Error al actualizar tarea: {e}")
            return False
    
    def eliminar_tarea(self, tarea_id):
        """
        Elimina una tarea de la base de datos
        
        Args:
            tarea_id (int): ID de la tarea a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            with sqlite3.connect(self.nombre_db) as conexion:
                cursor = conexion.cursor()
                
                cursor.execute('DELETE FROM tareas WHERE id = ?', (tarea_id,))
                
                if cursor.rowcount > 0:
                    conexion.commit()
                    print(f"✅ Tarea ID {tarea_id} eliminada correctamente")
                    return True
                else:
                    print(f"⚠️ No se encontró la tarea con ID {tarea_id}")
                    return False
                    
        except sqlite3.Error as e:
            print(f"❌ Error al eliminar tarea: {e}")
            return False
    
    def marcar_completada(self, tarea_id, completada=True):
        """
        Marca una tarea como completada o no completada
        
        Args:
            tarea_id (int): ID de la tarea
            completada (bool): True para marcar como completada, False para desmarcar
            
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            estado_completada = 1 if completada else 0
            
            with sqlite3.connect(self.nombre_db) as conexion:
                cursor = conexion.cursor()
                
                cursor.execute('''
                    UPDATE tareas
                    SET completada = ?, fecha_actualizacion = ?
                    WHERE id = ?
                ''', (estado_completada, fecha_actual, tarea_id))
                
                if cursor.rowcount > 0:
                    conexion.commit()
                    estado_texto = "completada" if completada else "pendiente"
                    print(f"✅ Tarea ID {tarea_id} marcada como {estado_texto}")
                    return True
                else:
                    print(f"⚠️ No se encontró la tarea con ID {tarea_id}")
                    return False
                    
        except sqlite3.Error as e:
            print(f"❌ Error al marcar tarea: {e}")
            return False
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas de las tareas
        
        Returns:
            dict: Diccionario con estadísticas
        """
        try:
            with sqlite3.connect(self.nombre_db) as conexion:
                cursor = conexion.cursor()
                
                # Total de tareas
                cursor.execute('SELECT COUNT(*) FROM tareas')
                total = cursor.fetchone()[0]
                
                # Tareas completadas
                cursor.execute('SELECT COUNT(*) FROM tareas WHERE completada = 1')
                completadas = cursor.fetchone()[0]
                
                # Tareas pendientes
                pendientes = total - completadas
                
                return {
                    'total': total,
                    'completadas': completadas,
                    'pendientes': pendientes
                }
                
        except sqlite3.Error as e:
            print(f"❌ Error al obtener estadísticas: {e}")
            return {'total': 0, 'completadas': 0, 'pendientes': 0}
    
    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos
        """
        # SQLite maneja automáticamente las conexiones con el context manager
        print("🔒 Conexión a la base de datos cerrada")


# Función de prueba para verificar el funcionamiento
def probar_gestor():
    """
    Función para probar todas las operaciones del gestor
    """
    print("🧪 Probando el gestor de tareas...")
    
    gestor = GestorTareas()
    
    # Agregar tareas de prueba
    gestor.agregar_tarea("Estudiar Python", "Completar el curso de Python básico")
    gestor.agregar_tarea("Hacer ejercicio", "Correr 30 minutos")
    gestor.agregar_tarea("Comprar comida", "Ir al supermercado")
    
    # Obtener todas las tareas
    tareas = gestor.obtener_todas_tareas()
    print(f"\n📋 Total de tareas: {len(tareas)}")
    
    for tarea in tareas:
        print(f"ID: {tarea[0]}, Título: {tarea[1]}, Completada: {'Sí' if tarea[3] else 'No'}")
    
    # Obtener estadísticas
    stats = gestor.obtener_estadisticas()
    print(f"\n📊 Estadísticas: {stats}")
    
    print("✅ Prueba completada")


if __name__ == "__main__":
    probar_gestor()
