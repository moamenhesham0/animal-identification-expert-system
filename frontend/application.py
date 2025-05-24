from PyQt6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QLabel,
    QRadioButton, QPushButton, QButtonGroup,
    QScrollArea, QApplication
)
from PyQt6.QtCore import Qt
import sys
import pyswip



class AnimalExpertSystem(QWidget):
    CRITERIA = {
        "Habitat" : "habitat",
        "Body Covering" : "skin_cover",
        "Reproduction Type" : "birth_type",
        "Number of Limbs" : "legs",
        "Flight Capability" : "canfly",
        "Diet" : "diet",
        "Defense Mechanism" : "behavior",
        "Communication Method" : "sound",
        "Special Adaptation" : "special",
        "Activity Pattern" : "activity"
    }

    QUESTION_TEMPLATE = "What is the {} of the animal?"

    VAR = "X"
    GET_CRITERIA_CHOICES_TEMPLATE = "extract_unique({}, _, {})"

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

    def __assert(criterion , storage):
        return AnimalExpertSystem.ASSERT_TEMPLATE.format(storage, criterion)

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

        self.choices = []
        self.results = []

        # PROGLOG INITIALIZATION

        self.prolog = pyswip.Prolog()
        self.prolog.consult("backend/backend.pl")

        # Init Choices
        for i, criterion in enumerate(AnimalExpertSystem.CRITERIA.values()):
            # Start index from 1, skip index 1 (animal name)
            # i from 0 to 9, so i+2 from 1+1=2 to 9+2=11 (Prolog: 2=habitat, ..., 11=activity)
            prolog_index = i + 2
            for sol in self.prolog.query(AnimalExpertSystem.GET_CRITERIA_CHOICES_TEMPLATE.format(prolog_index, AnimalExpertSystem.VAR)):
                def decode_val(val):
                    if isinstance(val, bytes):
                        return val.decode('utf-8')
                    return str(val)
                self.choices.append([decode_val(val) for val in sol[AnimalExpertSystem.VAR]])
                break




        # GUI Initialization
        self.setStyleSheet("background-color: #f5f5f5;")



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
        # Show user's answers
        result_label_header = QLabel("Your Answers")
        result_label_header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(result_label_header)

        for result in self.results:
            result_label = QLabel(result)
            result_label.setStyleSheet("font-size: 18px; color: #444;")
            self.layout.addWidget(result_label)

        # Visually distinct break
        self.layout.addWidget(AnimalExpertSystem.__create_break_line())

        # Query Prolog for all animal scores and find the best match(es)
        matches = []
        def decode_val(val):
            if isinstance(val, bytes):
                return val.decode('utf-8')
            return str(val)
        for sol in self.prolog.query("animal_score(Name, Score)"):
            name = sol["Name"]
            score = sol["Score"]
            name = decode_val(name)
            matches.append((name, score))
        if not matches:
            best_animals = []
            max_score = None
        else:
            max_score = max(score for _, score in matches)
            best_animals = [name for name, score in matches if score == max_score]
        # Show best-matching animal(s) and their score
        match_header = QLabel("Best-Matching Animal(s)")
        match_header.setStyleSheet("font-size: 22px; font-weight: bold; color: #4CAFAF; margin-top: 20px;")
        
        self.layout.addWidget(match_header)

        if not best_animals or max_score is None or max_score <= 0:
            no_match_label = QLabel("No animals matched your answers.")
            no_match_label.setStyleSheet("font-size: 18px; color: #b00; font-weight: bold;")
            self.layout.addWidget(no_match_label)
        else:
            for animal in best_animals:
                animal_label = QLabel(f"{animal} (Match score: {max_score})")
                animal_label.setStyleSheet("font-size: 20px; color: #228B22; font-weight: bold; margin-bottom: 6px;")
                self.layout.addWidget(animal_label)


    def get_unique_criterion_values(self, index):
        # Returns unique values for a criterion index (1-based)
        result = []
        for sol in self.prolog.query(f"extract_unique({index}, _, List)"):
            result = [str(val) for val in sol['List']]
        print(result)
        return result

    def submit_handler(self):
        # Clear previous answers in Prolog
        list(self.prolog.query("retractall(asked(_, _, _))."))

        # Assert user answers for each criterion
        self.results = []
        for i, (criterion_label, criterion_key) in enumerate(self.CRITERIA.items()):
            selected = None
            for btn in self.button_groups[i].buttons():
                if btn.isChecked():
                    selected = btn.text()
                    # Decode if bytes (shouldn't be needed after above, but safe)
                    if isinstance(selected, bytes):
                        selected = selected.decode('utf-8')
                    break
            if selected is not None:
                self.prolog.assertz(f'asked(user, {criterion_key}, "{selected}")')
                self.results.append(f"{criterion_label}: {selected}")
            else:
                # If not answered, still show in results
                self.results.append(f"{criterion_label}: (no answer)")

        # Get recommendations (capture output from Prolog)
        # To get results in Python, you need to add a new predicate in Prolog that returns the matches as a list.
        # For now, this will just print to the console:
        list(self.prolog.query("recommend_animals."))

        self.__set_button("Back", self.back_handler)
        self.result_window()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimalExpertSystem()
    window.setWindowTitle("Animal Expert System")
    window.show()
    sys.exit(app.exec())
