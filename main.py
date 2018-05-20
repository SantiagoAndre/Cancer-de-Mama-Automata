import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi

class FormEncuentas(QDialog):
    def __init__(self, parent = None):
        super(FormEncuentas, self).__init__()
        # Carga el archivo xml encuesta.ui
        loadUi('encuesta.ui', self)
        # Asigna un titulo a la interfaz
        self.setWindowTitle('Cancer de mama')
        self.setWindowIcon(QtGui.QIcon('ico-cancer_mama.png'))
        # Conecta el boton a la clase FormEncuentas
        self.BtnEnviarEncuesta.clicked.connect(self.enviar_formulario)

        # Inicializa variables a utilizar
        self.numero_celula = 0
        self.diccionario_respuestas = {
                                        self.ckb_1positiva: 20,
                                        self.ckb_2positiva: 12.5,
                                        self.ckb_3positiva: 12.5,
                                        self.ckb_4positiva: 12,
                                        self.ckb_5positiva: 8,
                                        self.ckb_6positiva: 5,
                                        self.ckb_7positiva: 7.5,
                                        self.ckb_8Negativa: 7.5,
                                        self.ckb_9positiva: 10,
                                        self.ckb_10positiva: 5
                                        }

    # Decorador
    # Alterar el funcionamiento original de la función que se pasa como parámetro
    @pyqtSlot()
    def enviar_formulario(self):
        """
        Verifica si las casillas agregadas al diccionario han sido seleccionadas,
        si es así, suma el valor del diccionario asociado al checkbox
        """
        contador=0
        # Itera los objetos checkbox del diccionario_respuestas
        for respuesta in self.diccionario_respuestas:
            # Verifica si ha sido seleccionada
            if respuesta.isChecked():
                # aumento contador para sacar cuantos si escogio
                contador=contador+1
                # Suma el valor contenido del diccionario_respuestas
                self.numero_celula += self.diccionario_respuestas[respuesta]
        # se enviaran los datos a una nueva funcion
        print("el numero de celulas es ",int(self.numero_celula))

        return int(self.numero_celula)

class	prueba(QMainWindow):
	def __init__(self, parent = None):
		super(prueba, self).__init__()
		# Carga el archivo xml encuesta.ui
		loadUi('prueba.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form =FormEncuentas()
    form.show()
    sys.exit(app.exec_())
