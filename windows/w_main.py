from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy, QSpacerItem, QPushButton
from pages.p_statistics import PStatistics
from pages.p_concentration import PConcentration
from widgets.wg_button import WgButton
from PyQt6.QtCore import Qt

class WMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main")
        self.setGeometry(100, 100, 800, 600)

        # Centrar la ventana
        self.center()

        # Layout principal con dos asides (izquierda y derecha) y el contenido central
        main_layout = QHBoxLayout()

        # Crear aside izquierdo con botones
        self.left_sidebar = self.create_left_sidebar()
        main_layout.addWidget(self.left_sidebar)

        # Crear el widget central que mostrará las estadísticas
        self.central_widget = QStackedWidget()
        self.page_statistics = PStatistics(self)
        self.central_widget.addWidget(self.page_statistics)
        self.central_widget.setCurrentWidget(self.page_statistics)  # Establecer como página predeterminada

        # Cambiar el estilo del área central
        self.central_widget.setStyleSheet("background-color: white;")  # Fondo blanco puro
        main_layout.addWidget(self.central_widget)

        # Crear aside derecho con la página de concentración
        self.right_sidebar = self.create_right_sidebar()
        main_layout.addWidget(self.right_sidebar)

        # Contenedor principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def center(self):
        # Centrar la ventana en la pantalla
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()
        new_x = (screen_geometry.width() - window_geometry.width()) // 2
        new_y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(new_x, new_y)

    def create_left_sidebar(self):
        left_sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        # Título "Monk Mode"
        monk_mode_label = QLabel("Monk\nMode")
        monk_mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        monk_mode_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        monk_mode_label.setWordWrap(True)
        sidebar_layout.addWidget(monk_mode_label)

        # Espaciador
        sidebar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Botón "Bloquear"
        block_button = WgButton("Bloquear")
        block_button.clicked.connect(self.block_action)
        sidebar_layout.addWidget(block_button)

        # Botón "Actividades"
        activities_button = WgButton("Actividades")
        activities_button.clicked.connect(self.activities_action)
        sidebar_layout.addWidget(activities_button)

        # Botón para alternar entre modo oscuro y claro
        toggle_theme_button = QPushButton("Toggle Dark/Light")
        toggle_theme_button.clicked.connect(self.toggle_theme)
        sidebar_layout.addWidget(toggle_theme_button)

        left_sidebar.setLayout(sidebar_layout)
        left_sidebar.setMinimumWidth(100)
        left_sidebar.setMaximumWidth(200)
        left_sidebar.setStyleSheet("background-color: #FAF3E0;")  # Color hueso

        return left_sidebar

    def create_right_sidebar(self):
        right_sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        # Página de concentración
        self.page_concentration = PConcentration(self)
        sidebar_layout.addWidget(self.page_concentration)

        right_sidebar.setLayout(sidebar_layout)
        right_sidebar.setMinimumWidth(100)
        right_sidebar.setMaximumWidth(200)
        right_sidebar.setStyleSheet("background-color: #FAF3E0;")  # Color hueso

        return right_sidebar

    def toggle_theme(self):
        # Implementar la lógica para alternar entre el modo oscuro y claro
        pass

    def block_action(self):
        # Acción para el botón "Bloquear"
        pass

    def activities_action(self):
        # Acción para el botón "Actividades"
        pass
