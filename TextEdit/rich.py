from PySide import QtCore
import pyqode.python


class RichTextEdit(pyqode.python.QPythonCodeEdit):
    def __init__(self):
        super(RichTextEdit, self).__init__()
        self.key_enter_callback_list = []

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            for callback in self.key_enter_callback_list:
                callback()

        return super(RichTextEdit, self).keyPressEvent(event)

    def add_ener_callback(self, callback):
        self.key_enter_callback_list.append(callback)
