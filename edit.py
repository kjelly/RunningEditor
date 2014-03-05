import sys
from PySide import QtGui, QtCore


class Edit(QtGui.QTextEdit):

    def __init__(self):
        super(Edit, self).__init__()
        self.initUI()
        self.key_enter_callback_list = []

    def initUI(self):
        self.show()
        self.setText("")

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            for callback in self.key_enter_callback_list:
                callback()
            self.indent()
            return True


        return super(Edit, self).keyPressEvent(event)

    def add_ener_callback(self, callback):
        self.key_enter_callback_list.append(callback)

    def keyReleaseEvent(self, event):

        return super(Edit, self).keyReleaseEvent(event)

    def indent(self):
        text = self.toPlainText()
        lines = text.split('\n')
        if len(lines) < 1:
            return
        last_line = lines[-1]
        start_space_count = len(last_line) - len(last_line.lstrip())
        if len(last_line) > 0 and last_line[-1] == ':':
            start_space_count += 4
        self.append(' ' * start_space_count)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Edit()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()