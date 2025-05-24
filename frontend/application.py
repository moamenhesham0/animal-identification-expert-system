from PyQt6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QLabel,
    QRadioButton, QPushButton, QButtonGroup,
    QScrollArea, QApplication
)
from PyQt6.QtCore import Qt
import sys


class AnimalExpertSystem(QWidget):
    CRITERIA = [
        "Habitat Type", "Body Covering", "Reproduction Type",
        "Number of Limbs", "Flight Capability", "Diet",
        "Defense Mechanism", "Communication Method",
        "Special Adaptation", "Activity Pattern"
    ]

    QUESTION_TEMPLATE = "What is the {} of the animal?"

    RADIO_STYLE =    """
                        QRadioButton {
                            spacing: 8px;
                            font-size: 16px;
                            color: #333333;
                        }

                        QRadioButton::indicator {
                            width: 20px;
                            height: 20px;
                            border-radius: 10px;
                            border: 2px solid #4CAFAF;
                            background: white;
                        }

                        QRadioButton::indicator:hover {
                            border-color: #3c9e9e;
                        }

                        QRadioButton::indicator:checked {
                            background-color: #4CAFAF;
                            border: 2px solid #4CAFAF;
                        }

                        QRadioButton::indicator:checked:hover {
                            background-color: #3c9e9e;
                            border-color: #3c9e9e;
                        }
                    """


    SCROLL_AREA_STYLE = """
                        QScrollArea {
                            border: none;
                        }

                        QScrollBar:vertical {
                            background: #e0e0e0;
                            width: 12px;
                            margin: 0px;
                            border-radius: 6px;
                        }

                        QScrollBar::handle:vertical {
                            background: #4CAFAF;
                            min-height: 20px;
                            border-radius: 6px;
                        }

                        QScrollBar::handle:vertical:hover {
                            background: #3c9e9e;
                        }

                        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                            height: 0px;
                        }

                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                            background: none;
                        }
                    """

    BUTTON_STYLE = f"""
                    QPushButton {{
                        font-size: 18px;
                        background-color: #4CAFAF;
                        color: white;
                        padding: 12px;
                        border-radius: 8px;
                    }}
                    QPushButton:hover {{
                        background-color: #3c9e9e;
                    }}
                """

    def __question(criterion):
        return AnimalExpertSystem.QUESTION_TEMPLATE.format(criterion)

    def __create_break_line():
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("margin: 10px 0; background-color: #e0e0e0;")
        return line

    def __set_button(self, text, function):
        self.button.setText(text)
        self.button.setStyleSheet(AnimalExpertSystem.BUTTON_STYLE)
        # self.button.clicked.disconnect()
        self.button.clicked.connect(function)

    def __clear_layout(self):
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def submit_handler(self):
        self.__set_button("Back", self.back_handler)
        self.result_window()

    def back_handler(self):
        self.__clear_layout()
        self.__set_button("Submit", self.submit_handler)
        self.init_window()

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f5f5f5;")

        self.results = [res for res in AnimalExpertSystem.CRITERIA]
        self.choices = [[res for res in AnimalExpertSystem.CRITERIA] for _ in range(len(AnimalExpertSystem.CRITERIA))]

        self.button = QPushButton()
        self.__set_button("Submit", self.submit_handler)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.setMinimumSize(800, 800)
        self.scroll_area.setStyleSheet(AnimalExpertSystem.SCROLL_AREA_STYLE)


        self.scroll_content = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(12)
        self.scroll_content.setLayout(self.layout)
        self.scroll_area.setWidget(self.scroll_content)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(40)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.button)
        self.setLayout(self.main_layout)

        self.init_window()

    def init_window(self):
        title_label = QLabel("Animal Expert System")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #333;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

        self.button_groups = []

        for i, criterion in enumerate(AnimalExpertSystem.CRITERIA):
            criteria_label = QLabel(AnimalExpertSystem.__question(criterion))
            criteria_label.setStyleSheet("font-size: 18px; color: #444; font-weight: bold;")
            self.layout.addWidget(criteria_label)

            button_group = QButtonGroup(self)
            self.button_groups.append(button_group)

            for choice in self.choices[i]:
                radio_button = QRadioButton(choice)
                radio_button.setStyleSheet(AnimalExpertSystem.RADIO_STYLE)
                self.layout.addWidget(radio_button)
                button_group.addButton(radio_button)

            self.layout.addWidget(AnimalExpertSystem.__create_break_line())

    def result_window(self):
        self.__clear_layout()
        result_label_header = QLabel("Your Answers")
        result_label_header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(result_label_header)

        for result in self.results:
            result_label = QLabel(result)
            result_label.setStyleSheet("font-size: 18px; color: #444;")
            self.layout.addWidget(result_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimalExpertSystem()
    window.setWindowTitle("Animal Expert System")
    window.show()
    sys.exit(app.exec())
