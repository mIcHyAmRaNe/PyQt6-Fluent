# coding:utf-8
"""
Frameless text editor — full menus, status bar, and auto dark/light theming.
All dialogs use FramelessDialog so they match the OS theme too.
"""

import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QTextEdit,
    QFileDialog,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMenuBar,
    QStatusBar,
)

from pyqt_fluent import FramelessMainWindow, FramelessDialog


class ConfirmDialog(FramelessDialog):
    """Frameless confirmation dialog — replaces QMessageBox for theming"""

    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(380, 140)
        self.set_resize_enabled(False)

        self._result = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(QLabel(message))
        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self._save_btn = QPushButton("Save")
        self._discard_btn = QPushButton("Discard")
        self._cancel_btn = QPushButton("Cancel")

        for b in (self._save_btn, self._discard_btn, self._cancel_btn):
            b.setFixedSize(90, 30)
            btn_row.addWidget(b)

        layout.addLayout(btn_row)

        self._save_btn.clicked.connect(lambda: self._done("save"))
        self._discard_btn.clicked.connect(lambda: self._done("discard"))
        self._cancel_btn.clicked.connect(lambda: self._done("cancel"))

        self.title_bar.raise_()

    def _done(self, result):
        self._result = result
        self.accept()

    def result(self):
        return self._result


class AboutDialog(FramelessDialog):
    """Simple frameless about dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.set_resize_enabled(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.addWidget(QLabel("PyQt6 Frameless Editor"))
        layout.addWidget(QLabel("v0.9.0 — auto dark/light theming"))

        close_btn = QPushButton("OK")
        close_btn.setFixedSize(80, 28)
        close_btn.clicked.connect(self.accept)

        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(close_btn)
        layout.addLayout(row)

        self.title_bar.raise_()
        self.resize(280, 160)


class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Editor"
        self.filters = "Text Files (*.txt)"
        self.path = None

        # ── Central widget ────────────────────────────────────────
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # ── Integrate menu bar into the title bar ─────────────────
        self.setMenuWidget(self.title_bar)
        menu_bar = QMenuBar(self.title_bar)
        self.title_bar.layout().insertWidget(0, menu_bar, 0, Qt.AlignmentFlag.AlignLeft)
        self.title_bar.layout().insertStretch(1, 1)

        self._build_file_menu(menu_bar)
        self._build_edit_menu(menu_bar)
        self._build_help_menu(menu_bar)

        # ── Status bar ────────────────────────────────────────────
        status_bar = QStatusBar(self)
        status_bar.addWidget(QLabel("Ready"))
        self.setStatusBar(status_bar)

        self.setWindowTitle(f"Untitled — {self.title}")

    # ── Menus ─────────────────────────────────────────────────────

    def _build_file_menu(self, menu_bar):
        menu = menu_bar.addMenu("&File")

        act = QAction("&New", self)
        act.setShortcut("Ctrl+N")
        act.triggered.connect(self.new_document)
        menu.addAction(act)

        act = QAction("&Open...", self)
        act.setShortcut("Ctrl+O")
        act.triggered.connect(self.open_document)
        menu.addAction(act)

        act = QAction("&Save", self)
        act.setShortcut("Ctrl+S")
        act.triggered.connect(self.save_document)
        menu.addAction(act)

        menu.addSeparator()

        act = QAction("E&xit", self)
        act.setShortcut("Alt+F4")
        act.triggered.connect(self.close)
        menu.addAction(act)

    def _build_edit_menu(self, menu_bar):
        menu = menu_bar.addMenu("&Edit")

        act = QAction("&Undo", self)
        act.setShortcut("Ctrl+Z")
        act.triggered.connect(self.text_edit.undo)
        menu.addAction(act)

        act = QAction("&Redo", self)
        act.setShortcut("Ctrl+Y")
        act.triggered.connect(self.text_edit.redo)
        menu.addAction(act)

    def _build_help_menu(self, menu_bar):
        menu = menu_bar.addMenu("&Help")

        act = QAction("About", self)
        act.setShortcut("F1")
        act.triggered.connect(self._show_about)
        menu.addAction(act)

    # ── Document actions ──────────────────────────────────────────

    def new_document(self):
        if self._confirm_save():
            self.text_edit.clear()
            self.path = None
            self.setWindowTitle(f"Untitled — {self.title}")

    def open_document(self):
        filename, _ = QFileDialog.getOpenFileName(self, filter=self.filters)
        if not filename:
            return
        self.path = Path(filename)
        self.text_edit.setText(self.path.read_text(encoding="utf-8"))
        self.setWindowTitle(f"{self.path.name} — {self.title}")

    def save_document(self):
        if self.path:
            self.path.write_text(self.text_edit.toPlainText(), encoding="utf-8")
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Save", filter=self.filters)
        if filename:
            self.path = Path(filename)
            self.path.write_text(self.text_edit.toPlainText(), encoding="utf-8")
            self.setWindowTitle(f"{self.path.name} — {self.title}")

    def _confirm_save(self):
        if not self.text_edit.document().isModified():
            return True
        name = self.path.name if self.path else "Untitled"
        dlg = ConfirmDialog("Unsaved Changes", f"Save changes to {name}?", self)
        dlg.exec()
        r = dlg.result()
        if r == "cancel":
            return False
        if r == "save":
            self.save_document()
        return True

    def _show_about(self):
        AboutDialog(self).exec()

    def closeEvent(self, e):
        if self._confirm_save():
            super().closeEvent(e)
        else:
            e.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    window = MainWindow()
    window.resize(700, 500)
    window.show()
    sys.exit(app.exec())
