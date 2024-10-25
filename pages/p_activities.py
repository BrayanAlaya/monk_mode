from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QLineEdit
from widgets.wg_button import WgButton
from utils.json_manager import load_json, update_json_section
import json

class PActivities(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Configuración de la interfaz
        layout = QVBoxLayout()
        label = QLabel("Actividades de estudio")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        self.activities_list = QListWidget()  # Lista de actividades
        layout.addWidget(self.activities_list)

        self.activity_input = QLineEdit()  # Campo de entrada para nueva actividad
        self.activity_input.setPlaceholderText("Agregar nueva actividad...")
        layout.addWidget(self.activity_input)

        add_activity_button = WgButton("Agregar")  # Botón para agregar actividad
        add_activity_button.clicked.connect(self.add_activity)
        layout.addWidget(add_activity_button)

        delete_activity_button = WgButton("Borrar seleccionada")  # Botón para borrar actividad
        delete_activity_button.clicked.connect(self.delete_activity)
        layout.addWidget(delete_activity_button)

        self.setLayout(layout)
        self.load_activities_from_json()  # Cargar actividades desde JSON al inicializar

    def add_activity(self):
        """Agrega una nueva actividad a la lista."""
        activity_name = self.activity_input.text()  # Usar activity_input en lugar de new_activity_input
        if activity_name:
            self.activities_list.addItem(activity_name)  # Agregar actividad a la lista
            self.activity_input.clear()  # Limpiar el campo de entrada
            self.save_activities_to_json()  # Guardar cambios en el JSON cada vez que agregues

    def delete_activity(self):
        """Elimina la actividad seleccionada."""
        selected_item = self.activities_list.currentItem()  # Obtener el elemento seleccionado
        if selected_item:
            self.activities_list.takeItem(self.activities_list.row(selected_item))  # Eliminar el elemento de la lista
            self.save_activities_to_json()  # Guardar cambios en el JSON cada vez que elimines

    def save_activities_to_json(self):
        """Guarda las actividades actuales en un archivo JSON sin sobrescribir los otros datos."""
        # Cargar datos existentes
        data = load_json('data/user.json')
        
        # Obtener actividades actuales
        activities = [self.activities_list.item(i).text() for i in range(self.activities_list.count())]
        
        # Actualizar la sección 'activities'
        data['activities'] = activities
        
        # Guardar en JSON
        with open('data/user.json', 'w') as file:
            json.dump(data, file, indent=4)


    def load_activities_from_json(self):
        """Carga actividades desde el archivo JSON."""
        data = load_json('data/user.json')
        activities = data.get("activities", [])

        # Asegúrate de que activities es una lista antes de procesar
        if isinstance(activities, list):
            for activity in activities:
                self.activities_list.addItem(activity)  # Agregar cada actividad a la lista

    def get_data(self):
        """Método para obtener la lista de actividades."""
        return [self.activities_list.item(i).text() for i in range(self.activities_list.count())]  # Retornar actividades
