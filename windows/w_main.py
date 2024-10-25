from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy, QSpacerItem, QGraphicsOpacityEffect, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from pages.p_dashboard import PDashboard
from pages.p_concentration import PConcentration
from widgets.wg_button import WgButton
from windows.w_settings_dialog import WSettingsDialog

class WMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main")
        self.setGeometry(100, 100, 800, 600)

        # Centrar la ventana
        self.center()

        # Layout principal con un aside izquierdo y el contenido central
        main_layout = QHBoxLayout()

        # Crear aside izquierdo con la página de concentración y el botón de ajustes
        self.left_sidebar = self.create_left_sidebar()
        main_layout.addWidget(self.left_sidebar)

        # Crear un área de desplazamiento para la página de estadísticas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Crear el widget central que mostrará las estadísticas
        self.central_widget = QStackedWidget()
        self.page_statistics = PDashboard(self)
        scroll_area.setWidget(self.page_statistics)  # Añadir el dashboard al scroll
        self.central_widget.addWidget(scroll_area)
        self.central_widget.setCurrentWidget(scroll_area)

        # Aplicar estilo en blanco y negro
        self.central_widget.setStyleSheet("background-color: white; color: black;")

        main_layout.addWidget(self.central_widget)

        # Contenedor principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Crear la capa de fondo (overlay) para oscurecer cuando se abren los ajustes
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 128);")  # Semitransparente
        self.overlay.setGeometry(self.rect())
        self.overlay.setVisible(False)  # Ocultar por defecto

    def center(self):
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()
        new_x = (screen_geometry.width() - window_geometry.width()) // 2
        new_y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(new_x, new_y)

    def create_left_sidebar(self):
        left_sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        # Título "Monk Mode" en negro
        monk_mode_label = QLabel("Monk\nMode")
        monk_mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        monk_mode_label.setStyleSheet("font-size: 48px; font-weight: bold; color: black;")
        monk_mode_label.setWordWrap(True)
        sidebar_layout.addWidget(monk_mode_label)

        # Página de concentración
        self.page_concentration = PConcentration(self)
        sidebar_layout.addWidget(self.page_concentration)

        # Espaciador
        sidebar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Botón de ajustes (verde de WgButton)
        settings_button = WgButton("Ajustes")
        settings_button.clicked.connect(self.show_settings_dialog)
        sidebar_layout.addWidget(settings_button)

        left_sidebar.setLayout(sidebar_layout)
        left_sidebar.setMinimumWidth(200)
        left_sidebar.setMaximumWidth(300)
        left_sidebar.setStyleSheet("background-color: white;")

        return left_sidebar

    def show_settings_dialog(self):
        # Mostrar la capa oscura
        self.overlay.setVisible(True)
        
        dialog = WSettingsDialog(self)
        
        # Ocultar la capa oscura cuando el diálogo se cierra
        dialog.finished.connect(lambda: self.overlay.setVisible(False))
        
        dialog.exec()
