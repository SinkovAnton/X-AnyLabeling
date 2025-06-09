"""Dialog for configuring remote server URL."""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
)

from anylabeling.views.labeling.utils.qt import new_icon
from anylabeling.views.labeling.utils.style import (
    get_lineedit_style,
    get_ok_btn_style,
    get_cancel_btn_style,
)


class RemoteServerDialog(QDialog):
    """Allows the user to enter a remote server URL."""

    def __init__(self, parent=None, current_url: str = ""):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Set Remote Server"))
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)

        label = QLabel(self.tr("Enter remote server URL:"))
        layout.addWidget(label)

        self.url_input = QLineEdit(current_url)
        self.url_input.setPlaceholderText(self.tr("e.g. http://host:8000"))
        self.url_input.setStyleSheet(get_lineedit_style())
        layout.addWidget(self.url_input)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        ok_button = button_box.button(QDialogButtonBox.Ok)
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        if ok_button:
            ok_button.setStyleSheet(get_ok_btn_style())
            ok_button.setIcon(QIcon())
        if cancel_button:
            cancel_button.setStyleSheet(get_cancel_btn_style())
            cancel_button.setIcon(QIcon())
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_url(self) -> str:
        """Return the entered URL."""
        return self.url_input.text().strip()

