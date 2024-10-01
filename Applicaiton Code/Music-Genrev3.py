import sys
import joblib
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import  QIcon
import os

# Get the directory where the executable is located
base_path = os.path.dirname(os.path.abspath(__file__))

# Use relative paths for your files
model_path = os.path.join(base_path, 'stacking_modelv3.pkl')
scaler_path = os.path.join(base_path, 'scalerv2.pkl')
window_icon_path = os.path.join(base_path, 'window_icon.png')

class MusicGenreClassifier(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.load_model()
        self.setup_genre_mapping()

    def setupUi(self):
        self.setObjectName("MusicGenreClassifier")
        self.resize(500, 600)  # Increased size to accommodate larger fonts
        # Set the window icon
        self.setWindowIcon(QIcon(window_icon_path))  # You can use .png here

        self.setStyleSheet("""
            QWidget {
                background-color: rgb(181, 254, 255);
                font-size: 14px;
            }
            QLineEdit {
                background-color: rgb(170, 255, 127);
                border-radius: 10px;
                padding: 1px;
                font-size: 14px;
                min-height: 25px;
            }
            QPushButton {
                background-color: rgb(85, 255, 127);
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                min-height: 30px;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)  # Increased spacing between widgets
        self.input_fields = {}
        
        fields = [
            "Track Name", "Artist Name", "Popularity", "Danceability", "Energy",
            "Key", "Loudness", "Mode", "Speechiness", "Acousticness",
            "Instrumentalness", "Liveness", "Valence", "Tempo", "Duration_in min/ms"
        ]

        for field in fields:
            line_edit = QtWidgets.QLineEdit(self)
            line_edit.setPlaceholderText(f"Enter {field}")
            layout.addWidget(line_edit)
            self.input_fields[field] = line_edit

        self.predict_button = QtWidgets.QPushButton("Predict the Genre", self)
        self.predict_button.clicked.connect(self.predict_genre)
        layout.addWidget(self.predict_button)

        self.setLayout(layout)
        self.setWindowTitle("Music Genre Classification")

    def load_model(self):
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
        except FileNotFoundError as e:
            self.show_error(f"Model file not found: {e}")
        except Exception as e:
            self.show_error(f"Error loading model: {e}")

    def setup_genre_mapping(self):
        # Create a mapping from numeric labels to genre names
        self.genre_mapping = {
            0: "Pop",
            1: "Rock",
            2: "Hip Hop",
            3: "Electronic",
            4: "Classical",
            5: "Jazz",
            6: "R&B",
            7: "Country",
            8: "Metal",
            9: "Folk",
            10: "Blues"
        }
        
    def predict_genre(self):
        try:
            input_data = self.get_input_data()
            if input_data:
                df = pd.DataFrame([input_data])
                input_scaled = self.scaler.transform(df)
                input_frame = pd.DataFrame(input_scaled, columns=df.columns,index=df.index)
                prediction = self.model.predict(input_frame)
                genre_number = prediction[0]
                genre_name = self.get_genre_name(genre_number)
                self.show_result(genre_name)
        except Exception as e:
            self.show_error(f"Prediction error: {e}")
            
    def get_genre_name(self, genre_number):
        return self.genre_mapping.get(genre_number, "Unknown Genre")
    
    def get_input_data(self):
        input_data = {}
        numeric_fields = [
            'Popularity', "Danceability", "Energy", "Key", "Loudness", "Mode",
            "Speechiness", "Acousticness", "Instrumentalness", "Liveness",
            "Valence", "Tempo", "Duration_in min/ms"
        ]
        for field in numeric_fields:
            value = self.input_fields[field].text().strip()
            if not value:
                self.show_error(f"Please enter a value for {field}")
                return None
            try:
                input_data[field.lower()] = float(value)
            except ValueError:
                self.show_error(f"Invalid input for {field}. Please enter a numeric value.")
                return None

        return input_data

    def show_result(self, genre):
        msg = QMessageBox(self)
        msg.setWindowTitle("Prediction Result")
        msg.setText(f"<h2>Predicted Genre: {genre}</h2>")
        msg.setStyleSheet("QLabel{min-width: 350px; font-size: 18px;}")
        msg.exec_()

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    classifier = MusicGenreClassifier()
    classifier.show()
    sys.exit(app.exec_())