import cv2
import json
import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from widgets.wg_button import WgButton
from windows.w_main import WMain  # Importar MainWindow

class WLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(600, 400)
        self.center_window()

        # Crear layout principal
        main_layout = QHBoxLayout()
        left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()

        # Título en la columna izquierda
        self.title_label = QLabel("MONK\nMODE", self)
        title_font = QFont("Arial", 40, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_column.addStretch()  # Añadir espacio flexible
        left_column.addWidget(self.title_label)
        left_column.addStretch()  # Añadir espacio flexible

        # Cargar datos de usuario y mostrar la interfaz correspondiente
        self.user_data = self.load_user()

        if self.user_data:
            self.right_column.addWidget(self.create_login_interface())
        else:
            self.right_column.addWidget(self.create_account_interface())

        # Añadir columnas al layout principal
        main_layout.addLayout(left_column, 1)
        main_layout.addLayout(self.right_column, 1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_login_interface(self):
        # Mensaje de bienvenida
        self.welcome_label = QLabel(f"Bienvenido, {self.user_data['name']}", self)  # Usar 'name'
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setWordWrap(True)
        welcome_font = QFont("Arial", 24)
        self.welcome_label.setFont(welcome_font)

        # Botón de login
        self.login_button = WgButton("Iniciar Sesión", self)
        self.login_button.clicked.connect(self.on_login)

        login_layout = QVBoxLayout()
        login_layout.addWidget(self.welcome_label)
        login_layout.addWidget(self.login_button)

        widget = QWidget()
        widget.setLayout(login_layout)
        return widget

    def create_account_interface(self):
        # Entradas para registrar cuenta
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nombre de Usuario")
        
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Botón de registrar cuenta
        self.register_button = WgButton("Registrar Cuenta", self)
        self.register_button.clicked.connect(self.on_register)

        account_layout = QVBoxLayout()
        account_layout.addWidget(self.username_input)
        account_layout.addWidget(self.password_input)
        account_layout.addWidget(self.register_button)

        widget = QWidget()
        widget.setLayout(account_layout)
        return widget

    def load_user(self):
        path = 'database/userData.json'  # Actualizar la ruta del archivo
        if os.path.exists(path):
            try:
                with open(path, 'r') as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error al cargar el archivo: {e}")
        return None

    def save_user(self, username, password):
        # Verificar y crear el directorio de fotos si no existe
        photos_dir = 'database/photos/'
        if not os.path.exists(photos_dir):
            os.makedirs(photos_dir)

        # Tomar la foto y guardarla
        photo_path = os.path.join(photos_dir, f"{username}.jpg")
        self.take_photo(photo_path)

        user_data = {"name": username, "password": password, "photo": photo_path}  # Guardar la ruta de la foto
        try:
            with open('database/userData.json', 'w') as file:  # Actualizar la ruta del archivo
                json.dump(user_data, file, indent=4)
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def take_photo(self, photo_path):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se puede acceder a la cámara.")
            return

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(photo_path, frame)
            print(f"Foto guardada en {photo_path}")
        else:
            print("Error al capturar la imagen.")
        cap.release()

    def compare_photos(self, img1_path, img2_path):
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        if img1 is None:
            print(f"No se pudo cargar la imagen {img1_path}")
            return False

        if img2 is None:
            print(f"No se pudo cargar la imagen {img2_path}")
            return False

        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Comparar las imágenes (puedes ajustar el método)
        diff = cv2.absdiff(img1_gray, img2_gray)
        if cv2.countNonZero(diff) < 1000:  # Ajusta el umbral según sea necesario
            return True
        return False

    def center_window(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def on_login(self):
        if self.user_data:
            registered_photo_path = self.user_data['photo']
            current_photo_path = 'current_photo.jpg'  # Foto tomada en el momento del login

            self.take_photo(current_photo_path)

            if self.compare_photos(current_photo_path, registered_photo_path):
                self.main_window = WMain()  # Inicializar la ventana principal
                self.main_window.show()
                self.close()  # Cerrar la ventana de inicio de sesión
            else:
                print("Las fotos no coinciden. Intenta de nuevo.")
        else:
            print("No hay usuario registrado.")

    def on_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            self.save_user(username, password)
            print("¡Cuenta creada exitosamente!")
            self.user_data = self.load_user()  # Cargar los datos actualizados
            self.right_column.itemAt(0).widget().deleteLater()  # Limpiar la interfaz anterior
            self.right_column.addWidget(self.create_login_interface())
        else:
            print("Por favor, completa todos los campos.")
