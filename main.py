import sys
from PySide import QtGui, QtCore
from TextEdit import Editor
from multiprocessing import Queue, Process
import threading
from core import catch_local_vars


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_editor = Editor()
        self.setCentralWidget(self.main_editor)
        self.createDockWindows()
        self.timer = QtCore.QTimer()

        self.process = None
        self.process_queue = None
        self.count = 0
        self.lock = threading.RLock()
        self.timer.timeout.connect(self.catch_local_vars)
        self.timer.start(2000)

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
        if not self.lock.acquire(False):
            return
        print 'timeout'
        if self.process is None:
            self.count = 0
            line_number = self.main_editor.textCursor().blockNumber()
            code = self.main_editor.toPlainText()
            test_code = self.test_code_editor.toPlainText()
            self.process_queue = Queue()
            self.process = Process(target=self.asyn_catch_local_vars,
                                   args=(self.process_queue, code, test_code,
                                         line_number))
            self.process.start()

        if self.process.is_alive():
            self.count += 1
        else:
            try:
                err = self.process_queue.get_nowait()
                local_vars_info = self.process_queue.get_nowait()
                self.error_view.setText(str(err))
                self.local_vars_view.setText(str(local_vars_info))
                self.count = 0
            except Exception as e:
                print str(e)
                self.process.terminate()
                self.process = None
                self.count = 0
        if self.count > 2:
            self.process.terminate()
            self.process = None
        self.lock.release()

    def asyn_catch_local_vars(self, output, code, test_code, line_number):
        env, local_vars, err = catch_local_vars(code, stop=line_number)
        if err:
            output.put(str(err))
            output.put('')
            return
        env, local_vars, err = catch_local_vars(test_code, env=env)
        output.put(str(err))
        output.put(str(local_vars))


def main():
    app = QtGui.QApplication(sys.argv)

    ex = MainWindow()
    ex.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
