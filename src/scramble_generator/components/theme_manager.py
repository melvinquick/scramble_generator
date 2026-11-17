import os

from .qss_file_handler import QssFileHandler
from .yaml_file_handler import YamlFileHandler


class ThemeManager:
    def __init__(self, app_settings):
        self.settings = app_settings

        base = os.path.join(os.path.dirname(__file__), "..", "resources", "styles")
        self.themes = YamlFileHandler(
            os.path.join(base, "themes.yaml")
        ).load_yaml_file()
        self.stylesheet_template = QssFileHandler(
            os.path.join(base, "styles.qss")
        ).load_qss_file()

    def get_available_themes(self):
        return [name for name in self.themes.keys() if name != "general"]

    def get_current_theme_name(self):
        theme = self.settings.value("theme", "scramble_generator_dark", type=str)
        if theme not in self.themes or theme == "general":
            return "scramble_generator_dark"
        return theme

    def get_theme_tokens(self, theme_name=None):
        if theme_name is None:
            theme_name = self.get_current_theme_name()
        if theme_name not in self.themes or theme_name == "general":
            theme_name = "scramble_generator_dark"
        return {**self.themes[theme_name], **self.themes["general"]}

    def apply_theme(self, widget, theme_name=None):
        tokens = self.get_theme_tokens(theme_name)
        stylesheet = self.stylesheet_template
        for key, value in tokens.items():
            stylesheet = stylesheet.replace("{{" + key + "}}", str(value))
        widget.setStyleSheet(stylesheet)
        return tokens
