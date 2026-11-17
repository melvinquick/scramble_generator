from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from .card import Card
from .constants import (
    DEFAULT_NUM_MOVES,
    DEFAULT_PUZZLE_TYPE,
    NUM_MOVES_MAX,
    NUM_MOVES_MIN,
    PUZZLE_TYPES,
)


class PreferencesDialog(QDialog):
    theme_changed = Signal(str)

    def __init__(self, settings, theme_manager, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.theme_manager = theme_manager

        self.setWindowTitle("Preferences")
        self.setMinimumWidth(400)

        current_theme = self.theme_manager.get_current_theme_name()
        self.theme_manager.apply_theme(self, current_theme)

        self._create_widgets()
        self._load_current_settings()
        self._create_layout()

    def _create_widgets(self):
        self.theme_combo = QComboBox()
        for theme_name in self.theme_manager.get_available_themes():
            self.theme_combo.addItem(theme_name.replace("_", " ").title(), theme_name)
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)

        self.puzzle_combo = QComboBox()
        self.puzzle_combo.addItems(PUZZLE_TYPES)

        self.moves_spin = QSpinBox()
        self.moves_spin.setRange(NUM_MOVES_MIN, NUM_MOVES_MAX)

        self.autocopy_check = QCheckBox("Copy automatically after generation")

        self.close_button = QPushButton("Close")
        self.close_button.setObjectName("PrimaryButton")
        self.close_button.setMinimumHeight(36)
        self.close_button.clicked.connect(self.accept)

    def _load_current_settings(self):
        current_theme = self.theme_manager.get_current_theme_name()
        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        saved_puzzle = self.settings.value(
            "default_puzzle_type", DEFAULT_PUZZLE_TYPE, type=str
        )
        if saved_puzzle in PUZZLE_TYPES:
            self.puzzle_combo.setCurrentText(saved_puzzle)

        saved_moves = self.settings.value(
            "default_num_moves", DEFAULT_NUM_MOVES, type=int
        )
        self.moves_spin.setValue(saved_moves)

        saved_autocopy = self.settings.value("auto_copy", True, type=bool)
        self.autocopy_check.setChecked(saved_autocopy)

    def _create_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)

        # Appearance Card
        appearance_card = Card("Appearance")
        appearance_layout = QFormLayout()
        appearance_layout.setContentsMargins(0, 0, 0, 0)
        appearance_layout.addRow("Theme:", self.theme_combo)
        appearance_card.addLayout(appearance_layout)
        main_layout.addWidget(appearance_card)

        # Defaults Card
        defaults_card = Card("Defaults")
        defaults_layout = QFormLayout()
        defaults_layout.setContentsMargins(0, 0, 0, 0)
        defaults_layout.addRow("Default Puzzle:", self.puzzle_combo)
        defaults_layout.addRow("Default Moves:", self.moves_spin)
        defaults_layout.addRow("", self.autocopy_check)
        defaults_card.addLayout(defaults_layout)
        main_layout.addWidget(defaults_card)

        main_layout.addStretch()
        main_layout.addWidget(self.close_button)

    def _on_theme_changed(self):
        selected_theme = self.theme_combo.currentData()
        self.settings.setValue("theme", selected_theme)
        self.theme_changed.emit(selected_theme)
        self.theme_manager.apply_theme(self, selected_theme)

    def accept(self):
        self.settings.setValue("default_puzzle_type", self.puzzle_combo.currentText())
        self.settings.setValue("default_num_moves", self.moves_spin.value())
        self.settings.setValue("auto_copy", self.autocopy_check.isChecked())
        super().accept()
