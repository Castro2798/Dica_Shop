import datetime
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from dbPost import dbPost

app = QtWidgets.QApplication([])

telaTeste = uic.loadUi("tree.ui")



'''consultaSistema = list(map(str, dbPost.consulta_db("SELECT nmsistema FROM gerenciador.system ORDER BY nmsistema")))
dbPost.removeCarac(consultaSistema)
sistema = dbPost.removeCarac(consultaSistema)
tela.boxSistema.addItems(sistema)'''

'''consultaModulo = list(map(str, dbPost.consulta_db("SELECT dsmodulo FROM gerenciador.module ORDER BY dsmodulo")))
dbPost.removeCarac(consultaModulo)
modulo = dbPost.removeCarac(consultaModulo)
tela.boxModulo.addItems(modulo)'''



telaTeste.show()
app.exec()
# pyinstaller -w