import sys
from PySide import QtGui, QtCore
from TextEdit import Editor

from core import catch_local_vars


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_editor = Editor()
        self.main_editor.add_ener_callback(self.catch_local_vars)
        self.setCentralWidget(self.main_editor)
        self.createDockWindows()

    def createDockWindows(self):
        self.test_code_docker = QtGui.QDockWidget("Test Code", self)
        self.test_code_editor = QtGui.QTextEdit(self.test_code_docker)
        self.test_code_docker.setWidget(self.test_code_editor)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                           self.test_code_docker)

        self.local_vars_docker = QtGui.QDockWidget("Local vars", self)
        self.local_vars_view = QtGui.QTextEdit(self.local_vars_docker)
        self.local_vars_view.setReadOnly(True)
        self.local_vars_docker.setWidget(self.local_vars_view)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                           self.local_vars_docker)

        self.error_docker = QtGui.QDockWidget("error", self)
        self.error_view = QtGui.QTextEdit(self.error_docker)
        self.error_view.setReadOnly(True)
        self.error_docker.setWidget(self.error_view)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.error_docker)

    def catch_local_vars(self):
        line_numbere = self.main_editor.textCursor().blockNumber()
        code = self.main_editor.toPlainText()
        env, local_vars, err = catch_local_vars(code, stop=line_numbere)
        if err:
            self.error_view.setText(str(err))
        else:
            code = self.test_code_editor.toPlainText()
            env, local_vars, err = catch_local_vars(code, env=env)
            self.error_view.setText(str(err))
            self.local_vars_view.setText(str(local_vars))


def main():
    app = QtGui.QApplication(sys.argv)

    ex = MainWindow()
    ex.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
