import sys
from PySide import QtGui, QtCore


class SimpleTextEdit(QtGui.QTextEdit):

    def __init__(self):
        super(SimpleTextEdit, self).__init__()
        self.initUI()
        self.key_enter_callback_list = []

    def initUI(self):
        self.setText("")

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            for callback in self.key_enter_callback_list:
                callback()
            self.indent()
            return True

        return super(SimpleTextEdit, self).keyPressEvent(event)

    def add_ener_callback(self, callback):
        self.key_enter_callback_list.append(callback)

    def keyReleaseEvent(self, event):

        return super(SimpleTextEdit, self).keyReleaseEvent(event)

    def indent(self):
        line_number = self.textCursor().blockNumber()
        text = self.toPlainText()
        lines = text.split('\n')
        if len(lines) < 1:
            return
        last_line = lines[line_number]
        start_space_count = len(last_line) - len(last_line.lstrip())
        if len(last_line) > 0 and last_line[-1] == ':':
            start_space_count += 4
        lines.insert(line_number + 1, ' ' * start_space_count)
        self.setText('\n'.join(lines))
        for i in xrange(line_number + 1):
            self.moveCursor(QtGui.QTextCursor.MoveOperation.Down)
        self.moveCursor(QtGui.QTextCursor.MoveOperation.EndOfLine)



def main():

    app = QtGui.QApplication(sys.argv)
    ex = SimpleTextEdit()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
