from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class Card(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)

        if title:
            title_label = QLabel(title)
            title_label.setObjectName("CardTitle")
            self.layout.addWidget(title_label)

        # Prevent the card from being vertically squished
        self.setMinimumHeight(60)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def addLayout(self, layout):
        self.layout.addLayout(layout)
