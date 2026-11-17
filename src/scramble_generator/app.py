import os
import sys

from PySide6.QtCore import QSettings, Qt, QTime, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from .components.about_dialog import AboutDialog
from .components.card import Card
from .components.constants import (
    DEFAULT_NUM_MOVES,
    DEFAULT_PUZZLE_TYPE,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    NUM_MOVES_MAX,
    NUM_MOVES_MIN,
    PUZZLE_DEFAULT_MOVES,
    PUZZLE_TYPES,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from .components.preferences_dialog import PreferencesDialog
from .components.scramble_generator import ScrambleGenerator as SG
from .components.theme_manager import ThemeManager


class ScrambleGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        config_dir = os.path.expanduser("~/.config/scramble_generator")
        os.makedirs(config_dir, exist_ok=True)
        settings_path = os.path.join(config_dir, "settings.conf")

        self.settings = QSettings(settings_path, QSettings.Format.IniFormat)
        self.theme_manager = ThemeManager(self.settings)
        self.init_ui()

    def init_ui(self):
        self.show()
        self.setWindowTitle("Scramble Generator")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        self.is_running = False
        self.elapsed_time = QTime(0, 0)

        self._create_menu_bar()
        self._create_widgets()
        self._create_layouts()
        self._connect_signals()

        self.apply_theme(self.theme_manager.get_current_theme_name())
        self._load_settings_into_ui()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        generate_action = QAction("Generate Scramble", self)
        generate_action.setShortcut("Ctrl+G")
        generate_action.triggered.connect(self.get_moves)
        file_menu.addAction(generate_action)

        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menu_bar.addMenu("Edit")
        copy_action = QAction("Copy Scramble", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self._copy_scramble)
        edit_menu.addAction(copy_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About Scramble Generator", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        prefs_action = QAction("Preferences", self)
        prefs_action.setShortcut("Ctrl+,")
        prefs_action.triggered.connect(self.show_preferences)
        menu_bar.addAction(prefs_action)

    def _create_widgets(self):
        self.puzzle_type = QComboBox()
        self.puzzle_type.addItems(PUZZLE_TYPES)

        self.num_moves = QSpinBox()
        self.num_moves.setRange(NUM_MOVES_MIN, NUM_MOVES_MAX)

        self.scramble = QLabel(
            "", alignment=Qt.AlignmentFlag.AlignCenter, wordWrap=True
        )
        self.scramble.setObjectName("ScrambleOutput")

        self.scramble_scroll = QScrollArea()
        self.scramble_scroll.setWidgetResizable(True)
        self.scramble_scroll.setWidget(self.scramble)
        self.scramble_scroll.setObjectName("ScrambleScroll")
        self.scramble_scroll.setMinimumHeight(180)

        self.timer_button = QPushButton("Start Timer")
        self.timer_button.setShortcut("Space")

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)

        self.timer_output = QLabel("00:00.0", alignment=Qt.AlignmentFlag.AlignCenter)
        self.timer_output.setObjectName("TimerOutput")
        self.timer_output.setMinimumHeight(36)

        self.scramble_button = QPushButton("Generate Scramble")
        self.scramble_button.setShortcut("Ctrl+G")
        self.scramble_button.setObjectName("PrimaryButton")
        self.scramble_button.setMinimumHeight(40)

        self.timer = QTimer()
        self.timer.setInterval(100)

    def _create_layouts(self):
        main_widget = QWidget()
        main_widget.setObjectName("MainWindowContent")
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # This forces the layout to respect the minimum heights of its children
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        # 1. Puzzle Settings Card
        puzzle_card = Card("Puzzle Settings")
        puzzle_layout = QFormLayout()
        puzzle_layout.setContentsMargins(0, 0, 0, 0)
        puzzle_layout.addRow("Puzzle:", self.puzzle_type)
        puzzle_layout.addRow("Moves:", self.num_moves)
        puzzle_card.addLayout(puzzle_layout)
        layout.addWidget(puzzle_card)

        # 2. Timer Card
        timer_card = Card("Timer")
        timer_controls = QHBoxLayout()
        timer_controls.setSpacing(8)
        timer_controls.addWidget(self.timer_button)
        timer_controls.addWidget(self.reset_button)
        timer_card.addLayout(timer_controls)
        timer_card.addWidget(self.timer_output)
        layout.addWidget(timer_card)

        # 3. Generated Scramble Card
        output_card = Card("Generated Scramble")
        output_card.addWidget(self.scramble_scroll)
        layout.addWidget(output_card, 1)  # stretch factor 1 makes this expand

        # 4. Bottom Button
        layout.addWidget(self.scramble_button)

        self.setCentralWidget(main_widget)

    def _connect_signals(self):
        self.scramble_button.clicked.connect(self.get_moves)
        self.puzzle_type.currentTextChanged.connect(self.set_default_num_moves)
        self.timer_button.clicked.connect(self.toggle_timer)
        self.timer.timeout.connect(self.update_time)

    def _load_settings_into_ui(self):
        saved_puzzle = self.settings.value(
            "default_puzzle_type", DEFAULT_PUZZLE_TYPE, type=str
        )
        if saved_puzzle in PUZZLE_TYPES:
            self.puzzle_type.setCurrentText(saved_puzzle)

        saved_moves = self.settings.value(
            "default_num_moves", DEFAULT_NUM_MOVES, type=int
        )
        self.num_moves.setValue(saved_moves)

    def show_preferences(self):
        dialog = PreferencesDialog(self.settings, self.theme_manager, self)
        dialog.theme_changed.connect(self.apply_theme)
        dialog.exec()

    def show_about(self):
        theme_name = self.theme_manager.get_current_theme_name()
        tokens = self.theme_manager.get_theme_tokens(theme_name)
        theme_color = tokens.get("accent-color", "#2F81F7")

        dialog = AboutDialog(theme_color, self)
        self.theme_manager.apply_theme(dialog, theme_name)
        dialog.exec()

    def _copy_scramble(self):
        text = self.scramble.text()
        if text:
            QApplication.clipboard().setText(text)

    def apply_theme(self, theme_name):
        self.theme_manager.apply_theme(self, theme_name)

    def get_moves(self):
        puzzle = self.puzzle_type.currentText().lower()
        num_moves = self.num_moves.value()

        scramble = SG(puzzle).generate_scramble(puzzle, num_moves)
        self.scramble.setText(scramble)

        auto_copy = self.settings.value("auto_copy", True, type=bool)
        if auto_copy:
            self._copy_scramble()

    def set_default_num_moves(self):
        puzzle = self.puzzle_type.currentText().lower()
        if puzzle in PUZZLE_DEFAULT_MOVES:
            self.num_moves.setValue(PUZZLE_DEFAULT_MOVES[puzzle])

    def toggle_timer(self):
        if not self.is_running:
            self.timer.start()
            self.timer_button.setText("Stop Timer")
            self.is_running = True
        else:
            self.timer.stop()
            self.timer_button.setText("Start Timer")
            self.is_running = False

    def reset_timer(self):
        self.timer.stop()
        self.timer_button.setText("Start Timer")
        self.is_running = False
        self.elapsed_time = QTime(0, 0)
        self.timer_output.setText("00:00.0")

    def update_time(self):
        self.elapsed_time = self.elapsed_time.addMSecs(100)
        self.timer_output.setText(self.elapsed_time.toString("mm:ss.z"))


def main():
    app = QApplication(sys.argv)
    main_window = ScrambleGenerator()  # noqa: F841
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
