import sys
from core import catch_local_vars
from PySide import QtGui, QtCore


class Edit(QtGui.QTextEdit):

    def __init__(self):
        super(Edit, self).__init__()
        self.initUI()

    def initUI(self):
        self.show()
        self.setText("")

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            line_numbere = self.textCursor().blockNumber()
            code = self.toPlainText()
            env, local_vars, err = catch_local_vars(code, stop=line_numbere)
            print local_vars
            print err
        return super(Edit, self).keyPressEvent(event)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Edit()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()