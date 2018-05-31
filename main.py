import sys
from PyQt5.QtWidgets import QApplication
from business.encuesta import FormEncuentas

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form =FormEncuentas()
    form.show()
    sys.exit(app.exec_())
