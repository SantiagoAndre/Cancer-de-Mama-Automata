from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from interface.interface_map import InterfaceNeighborhood
class FormEncuentas(QDialog):
    def __init__(self, parent = None):
        super(FormEncuentas, self).__init__()
        # Carga el archivo xml encuesta.ui
        loadUi('interface/encuesta.ui', self)
        # Asigna un titulo a la interfaz
        # Conecta el boton a la clase FormEncuentas
        self.BtnEnviarEncuesta.clicked.connect(self.enviar_formulario)

        self.diccionario_respuestas = {
                                        self.ckb_1positiva: 20,
                                        self.ckb_2positiva: 12.5,
                                        self.ckb_3positiva: 12.5,
                                        self.ckb_4positiva: 12,
                                        self.ckb_5positiva: 8,
                                        self.ckb_6positiva: 5,
                                        self.ckb_7negativa: 7.5,
                                        self.ckb_8Negativa: 7.5,
                                        self.ckb_9positiva: 10,
                                        self.ckb_10positiva: 5
                                        }
        self._map = None
    # Decorador
    # Alterar el funcionamiento original de la función que se pasa como parámetro
    @pyqtSlot()
    def enviar_formulario(self):
        """
        Verifica si las casillas agregadas al diccionario han sido seleccionadas,
        si es así, suma el valor del diccionario asociado al checkbox
        """
        numero_celulas=0
        # Itera los objetos checkbox del diccionario_respuestas
        for respuesta in self.diccionario_respuestas:
            # Verifica si ha sido seleccionada
            if respuesta.isChecked():
                # Suma el valor contenido del diccionario_respuestas
                numero_celulas += self.diccionario_respuestas[respuesta]
        # se enviaran los datos a una nueva funcion
        #print("el numero de celulas es ",int(numero_celulas))
        self._map = InterfaceNeighborhood(numero_celulas,100,100)
        self._map.start()
        return (self.numero_celula)
