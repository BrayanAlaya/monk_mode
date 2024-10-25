import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import json
import os
import unidecode  # Para quitar tildes
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class ChartRenderer(QWidget):
    def __init__(self, theme):
        super().__init__()
        self.theme = theme
        self.data = self.load_data()
        self.activities = self.load_user_activities()

        # Create the Matplotlib canvas and add it to the widget layout
        self.canvas = FigureCanvas(plt.Figure(figsize=(10, 8)))
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.render_chart()

    def load_data(self):
        """Load data from JSON based on the theme."""
        # Convert theme to lowercase and remove tildes
        file_theme = unidecode.unidecode(self.theme).lower()  
        file_path = f"data/history/{file_theme}.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            print(f"No data found for file: {file_path}")
            return {}

    def load_user_activities(self):
        """Load user activities from the user.json file."""
        user_file_path = 'data/history/user.json'
        if os.path.exists(user_file_path):
            with open(user_file_path, 'r') as file:
                user_data = json.load(file)
                # Convert activities to lowercase and remove tildes
                return [unidecode.unidecode(activity).lower() for activity in user_data.get("activities", [])]
        else:
            print(f"No user data found for file: {user_file_path}")
            return []

    def render_chart(self):
        """Generate and display the chart from the loaded data."""
        dates = list(self.data.keys())

        if not dates:  # Check if data is available
            print("No data available to render charts.")
            return

        durations = [self.data[date]["duration"] for date in dates]
        emotions = {key: [] for key in self.data[dates[0]]["emotions"].keys()}

        # Gather emotions data
        for date in dates:
            for emotion, value in self.data[date]["emotions"].items():
                emotions[emotion].append(value)

        # Use the canvas figure
        fig = self.canvas.figure
        fig.clear()  # Clear previous plots

        # Plot duration
        ax1 = fig.add_subplot(len(emotions) + 1, 1, 1)
        ax1.bar(dates, durations, color='skyblue')
        ax1.set_title(f'Study Duration - {self.theme.capitalize()}')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Duration (minutes)')
        ax1.tick_params(axis='x', rotation=45)

        # Plot emotions
        for i, (emotion, values) in enumerate(emotions.items(), start=2):
            ax = fig.add_subplot(len(emotions) + 1, 1, i)
            ax.plot(dates, values, marker='o')
            ax.set_title(f'Emotion: {emotion.capitalize()}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Percentage (%)')
            ax.tick_params(axis='x', rotation=45)

        fig.tight_layout()
        self.canvas.draw()
