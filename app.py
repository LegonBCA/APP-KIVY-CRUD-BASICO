#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación To-Do con Kivy y SQLite
Interfaz de usuario principal
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from gestor import GestorTareas


class TareaWidget(BoxLayout):
    """
    Widget personalizado para mostrar una tarea individual
    """
    
    def __init__(self, tarea_data, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.tarea_data = tarea_data
        self.app = app_instance
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60
        self.spacing = 10
        self.padding = [10, 5]
        
        self.crear_widgets()
    
    def crear_widgets(self):
        """
        Crea los widgets para mostrar la tarea
        """
        tarea_id, titulo, descripcion, completada, fecha_creacion, fecha_actualizacion = self.tarea_data
        
        # Checkbox para marcar como completada
        self.checkbox = CheckBox(active=bool(completada))
        self.checkbox.bind(active=self.on_checkbox_change)
        
        # Layout para el contenido de la tarea
        content_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        
        # Título de la tarea
        self.titulo_label = Label(
            text=f"[b]{titulo}[/b]",
            markup=True,
            size_hint_y=0.6,
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        
        # Descripción de la tarea
        self.descripcion_label = Label(
            text=descripcion if descripcion else "Sin descripción",
            size_hint_y=0.4,
            text_size=(None, None),
            halign='left',
            valign='middle',
            color=(0.6, 0.6, 0.6, 1)
        )
        
        content_layout.add_widget(self.titulo_label)
        content_layout.add_widget(self.descripcion_label)
        
        # Layout para los botones
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_x=0.4, spacing=5)
        
        # Botón Editar
        btn_editar = Button(
            text="Editar",
            size_hint_x=0.5,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_editar.bind(on_press=lambda x: self.app.editar_tarea(tarea_id))
        
        # Botón Eliminar
        btn_eliminar = Button(
            text="Eliminar",
            size_hint_x=0.5,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        btn_eliminar.bind(on_press=lambda x: self.app.eliminar_tarea(tarea_id))
        
        buttons_layout.add_widget(btn_editar)
        buttons_layout.add_widget(btn_eliminar)
        
        # Agregar todos los widgets al layout principal
        self.add_widget(self.checkbox)
        self.add_widget(content_layout)
        self.add_widget(buttons_layout)
        
        # Aplicar estilo si está completada
        if completada:
            self.aplicar_estilo_completada()
    
    def on_checkbox_change(self, instance, value):
        """
        Maneja el cambio en el checkbox
        """
        tarea_id = self.tarea_data[0]
        self.app.gestor.marcar_completada(tarea_id, value)
        self.app.actualizar_lista_tareas()
        
        if value:
            self.aplicar_estilo_completada()
        else:
            self.aplicar_estilo_pendiente()
    
    def aplicar_estilo_completada(self):
        """
        Aplica el estilo para tareas completadas
        """
        self.titulo_label.color = (0.4, 0.4, 0.4, 1)
        self.descripcion_label.color = (0.5, 0.5, 0.5, 1)
        self.canvas.before.clear()
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.9, 0.9, 0.9, 1)
            Rectangle(pos=self.pos, size=self.size)
    
    def aplicar_estilo_pendiente(self):
        """
        Aplica el estilo para tareas pendientes
        """
        self.titulo_label.color = (0, 0, 0, 1)
        self.descripcion_label.color = (0.6, 0.6, 0.6, 1)
        self.canvas.before.clear()


class TodoApp(App):
    """
    Aplicación principal To-Do
    """
    
    def build(self):
        """
        Construye la interfaz de usuario
        """
        self.title = "📝 App To-Do con SQLite"
        self.gestor = GestorTareas()
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título de la aplicación
        titulo = Label(
            text="📝 Mi App To-Do",
            font_size='24sp',
            size_hint_y=None,
            height=50,
            color=(0.2, 0.4, 0.8, 1)
        )
        
        # Layout para agregar nuevas tareas
        agregar_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        # Campo de título
        self.titulo_input = TextInput(
            hint_text="Título de la tarea...",
            size_hint_x=0.4,
            multiline=False
        )
        
        # Campo de descripción
        self.descripcion_input = TextInput(
            hint_text="Descripción (opcional)...",
            size_hint_x=0.4,
            multiline=False
        )
        
        # Botón agregar
        btn_agregar = Button(
            text="➕ Agregar",
            size_hint_x=0.2,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        btn_agregar.bind(on_press=self.agregar_tarea)
        
        agregar_layout.add_widget(self.titulo_input)
        agregar_layout.add_widget(self.descripcion_input)
        agregar_layout.add_widget(btn_agregar)
        
        # Estadísticas
        self.stats_label = Label(
            text="📊 Cargando estadísticas...",
            size_hint_y=None,
            height=30,
            color=(0.4, 0.4, 0.4, 1)
        )
        
        # ScrollView para la lista de tareas
        scroll = ScrollView()
        self.lista_tareas = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.lista_tareas.bind(minimum_height=self.lista_tareas.setter('height'))
        scroll.add_widget(self.lista_tareas)
        
        # Agregar widgets al layout principal
        main_layout.add_widget(titulo)
        main_layout.add_widget(agregar_layout)
        main_layout.add_widget(self.stats_label)
        main_layout.add_widget(scroll)
        
        # Cargar tareas iniciales
        Clock.schedule_once(lambda dt: self.actualizar_lista_tareas(), 0.1)
        
        return main_layout
    
    def agregar_tarea(self, instance):
        """
        Agrega una nueva tarea
        """
        titulo = self.titulo_input.text.strip()
        descripcion = self.descripcion_input.text.strip()
        
        if not titulo:
            self.mostrar_mensaje("⚠️ Error", "Por favor ingresa un título para la tarea.")
            return
        
        if self.gestor.agregar_tarea(titulo, descripcion):
            self.titulo_input.text = ""
            self.descripcion_input.text = ""
            self.actualizar_lista_tareas()
            self.mostrar_mensaje("✅ Éxito", f"Tarea '{titulo}' agregada correctamente.")
        else:
            self.mostrar_mensaje("❌ Error", "No se pudo agregar la tarea.")
    
    def actualizar_lista_tareas(self):
        """
        Actualiza la lista de tareas en la interfaz
        """
        # Limpiar lista actual
        self.lista_tareas.clear_widgets()
        
        # Obtener tareas de la base de datos
        tareas = self.gestor.obtener_todas_tareas()
        
        if not tareas:
            # Mostrar mensaje si no hay tareas
            no_tareas_label = Label(
                text="📝 No hay tareas. ¡Agrega tu primera tarea!",
                size_hint_y=None,
                height=100,
                color=(0.6, 0.6, 0.6, 1)
            )
            self.lista_tareas.add_widget(no_tareas_label)
        else:
            # Agregar cada tarea como widget
            for tarea in tareas:
                tarea_widget = TareaWidget(tarea, self)
                self.lista_tareas.add_widget(tarea_widget)
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
    
    def actualizar_estadisticas(self):
        """
        Actualiza las estadísticas mostradas
        """
        stats = self.gestor.obtener_estadisticas()
        self.stats_label.text = f"📊 Total: {stats['total']} | ✅ Completadas: {stats['completadas']} | ⏳ Pendientes: {stats['pendientes']}"
    
    def editar_tarea(self, tarea_id):
        """
        Abre un popup para editar una tarea
        """
        tarea = self.gestor.obtener_tarea_por_id(tarea_id)
        if not tarea:
            self.mostrar_mensaje("❌ Error", "No se pudo encontrar la tarea.")
            return
        
        # Crear popup de edición
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Título del popup
        titulo_popup = Label(
            text=f"✏️ Editar Tarea #{tarea_id}",
            size_hint_y=None,
            height=40,
            color=(0.2, 0.4, 0.8, 1)
        )
        
        # Campo de título
        titulo_input = TextInput(
            text=tarea[1],
            hint_text="Título de la tarea...",
            size_hint_y=None,
            height=40,
            multiline=False
        )
        
        # Campo de descripción
        descripcion_input = TextInput(
            text=tarea[2] or "",
            hint_text="Descripción (opcional)...",
            size_hint_y=None,
            height=40,
            multiline=False
        )
        
        # Layout para botones
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        # Botón Guardar
        btn_guardar = Button(
            text="💾 Guardar",
            background_color=(0.2, 0.8, 0.2, 1)
        )
        
        # Botón Cancelar
        btn_cancelar = Button(
            text="❌ Cancelar",
            background_color=(0.8, 0.2, 0.2, 1)
        )
        
        buttons_layout.add_widget(btn_guardar)
        buttons_layout.add_widget(btn_cancelar)
        
        # Agregar widgets al popup
        popup_layout.add_widget(titulo_popup)
        popup_layout.add_widget(titulo_input)
        popup_layout.add_widget(descripcion_input)
        popup_layout.add_widget(buttons_layout)
        
        # Crear y mostrar popup
        popup = Popup(
            title="",
            content=popup_layout,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        
        def guardar_cambios(instance):
            nuevo_titulo = titulo_input.text.strip()
            nueva_descripcion = descripcion_input.text.strip()
            
            if not nuevo_titulo:
                self.mostrar_mensaje("⚠️ Error", "El título no puede estar vacío.")
                return
            
            if self.gestor.actualizar_tarea(tarea_id, nuevo_titulo, nueva_descripcion, bool(tarea[3])):
                popup.dismiss()
                self.actualizar_lista_tareas()
                self.mostrar_mensaje("✅ Éxito", "Tarea actualizada correctamente.")
            else:
                self.mostrar_mensaje("❌ Error", "No se pudo actualizar la tarea.")
        
        def cancelar(instance):
            popup.dismiss()
        
        btn_guardar.bind(on_press=guardar_cambios)
        btn_cancelar.bind(on_press=cancelar)
        
        popup.open()
    
    def eliminar_tarea(self, tarea_id):
        """
        Muestra un popup de confirmación para eliminar una tarea
        """
        tarea = self.gestor.obtener_tarea_por_id(tarea_id)
        if not tarea:
            self.mostrar_mensaje("❌ Error", "No se pudo encontrar la tarea.")
            return
        
        # Crear popup de confirmación
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Mensaje de confirmación
        mensaje = Label(
            text=f"¿Estás seguro de que quieres eliminar la tarea:\n\n\"{tarea[1]}\"?",
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        
        # Layout para botones
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        # Botón Confirmar
        btn_confirmar = Button(
            text="🗑️ Eliminar",
            background_color=(0.8, 0.2, 0.2, 1)
        )
        
        # Botón Cancelar
        btn_cancelar = Button(
            text="❌ Cancelar",
            background_color=(0.6, 0.6, 0.6, 1)
        )
        
        buttons_layout.add_widget(btn_confirmar)
        buttons_layout.add_widget(btn_cancelar)
        
        # Agregar widgets al popup
        popup_layout.add_widget(mensaje)
        popup_layout.add_widget(buttons_layout)
        
        # Crear y mostrar popup
        popup = Popup(
            title="⚠️ Confirmar Eliminación",
            content=popup_layout,
            size_hint=(0.7, 0.4),
            auto_dismiss=False
        )
        
        def confirmar_eliminacion(instance):
            if self.gestor.eliminar_tarea(tarea_id):
                popup.dismiss()
                self.actualizar_lista_tareas()
                self.mostrar_mensaje("✅ Éxito", "Tarea eliminada correctamente.")
            else:
                self.mostrar_mensaje("❌ Error", "No se pudo eliminar la tarea.")
        
        def cancelar(instance):
            popup.dismiss()
        
        btn_confirmar.bind(on_press=confirmar_eliminacion)
        btn_cancelar.bind(on_press=cancelar)
        
        popup.open()
    
    def mostrar_mensaje(self, titulo, mensaje):
        """
        Muestra un popup con un mensaje
        """
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        mensaje_label = Label(
            text=mensaje,
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        
        btn_ok = Button(
            text="OK",
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        
        popup_layout.add_widget(mensaje_label)
        popup_layout.add_widget(btn_ok)
        
        popup = Popup(
            title=titulo,
            content=popup_layout,
            size_hint=(0.6, 0.3),
            auto_dismiss=False
        )
        
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()
    
    def on_stop(self):
        """
        Se ejecuta cuando la aplicación se cierra
        """
        self.gestor.cerrar_conexion()
        print("👋 Aplicación cerrada correctamente")
