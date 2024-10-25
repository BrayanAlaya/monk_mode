from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QLineEdit
from widgets.wg_button import WgButton
from utils.json_manager import load_json, update_json_section
import json

class PBlock(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Configuración de la interfaz
        layout = QVBoxLayout()
        label = QLabel("Aplicaciones bloqueadas")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        self.app_list = QListWidget()  # Lista de aplicaciones
        layout.addWidget(self.app_list)

        self.app_input = QLineEdit()  # Campo de entrada para nueva aplicación
        self.app_input.setPlaceholderText("Agregar nueva aplicación...")
        layout.addWidget(self.app_input)

        add_app_button = WgButton("Agregar")  # Botón para agregar aplicación
        add_app_button.clicked.connect(self.add_app)
        layout.addWidget(add_app_button)

        delete_app_button = WgButton("Borrar seleccionada")  # Botón para borrar aplicación
        delete_app_button.clicked.connect(self.delete_app)
        layout.addWidget(delete_app_button)

        self.setLayout(layout)
        self.load_apps_from_json()  # Cargar aplicaciones desde JSON al inicializar

    def add_app(self):
        """Agrega una nueva aplicación a la lista."""
        app_name = self.app_input.text()  # Cambiar new_app_input a app_input
        if app_name:
            self.app_list.addItem(app_name)  # Agregar aplicación a la lista
            self.app_input.clear()  # Limpiar el campo de entrada
            self.save_apps_to_json()  # Guardar cambios en el JSON cada vez que agregues

    def delete_app(self):
        """Elimina la aplicación seleccionada."""
        selected_item = self.app_list.currentItem()  # Obtener el elemento seleccionado
        if selected_item:
            self.app_list.takeItem(self.app_list.row(selected_item))  # Eliminar el elemento de la lista
            self.save_apps_to_json()  # Guardar cambios en el JSON cada vez que elimines

    def save_apps_to_json(self):
        """Guarda las aplicaciones actuales en un archivo JSON sin sobrescribir los otros datos."""
        # Cargar datos existentes
        data = load_json('data/user.json')
        
        # Obtener aplicaciones actuales
        apps = [self.app_list.item(i).text() for i in range(self.app_list.count())]
        
        # Actualizar la sección 'block'
        data['block'] = apps
        
        # Guardar en JSON
        with open('data/user.json', 'w') as file:
            json.dump(data, file, indent=4)


    def load_apps_from_json(self):
        """Carga aplicaciones desde el archivo JSON."""
        data = load_json('data/user.json')
        apps = data.get("block", [])

        # Asegúrate de que apps es una lista antes de procesar
        if isinstance(apps, list):
            for app in apps:
                self.app_list.addItem(app)  # Agregar cada aplicación a la lista

    def get_data(self):
        """Método para obtener la lista de aplicaciones bloqueadas."""
        return [self.app_list.item(i).text() for i in range(self.app_list.count())]  # Retornar aplicaciones
