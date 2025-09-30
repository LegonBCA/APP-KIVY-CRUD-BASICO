#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación To-Do con Kivy y SQLite
Archivo principal que ejecuta la aplicación
"""

from app import TodoApp


if __name__ == '__main__':
    print("🚀 Iniciando App To-Do con SQLite...")
    print("📱 Aplicación desarrollada con Kivy 2.3.1")
    print("🗄️ Base de datos: SQLite3")
    print("=" * 50)
    
    # Ejecutar la aplicación
    TodoApp().run()