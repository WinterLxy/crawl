from PyQt5.QtWidgets import *
import sys
import movie_search
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWinow = QMainWindow()
    ui = movie_search.Ui_MainWindow()
    ui.setupUi(mainWinow)
    mainWinow.show()
    sys.exit(app.exec_())

