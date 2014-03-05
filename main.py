import sys
from PySide import QtGui, QtCore
from edit import Edit


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Edit()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()