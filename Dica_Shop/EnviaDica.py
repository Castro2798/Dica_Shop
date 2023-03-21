import datetime
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from dbPost import dbPost
import Dica



def msgCampos():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText("Ops! \n\n"
                   "Verificamos que tem campos obrigatórios em branco, preencha-os para poder prosseguir!"
                   "    \n\nCampos:\n  -Título\n  -Descrição do problema/dúvida\n  -Descrição da resolução")
    msgBox.setWindowTitle("Aviso!!!")
    return msgBox.exec()

def msgSucesso():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Dica enviada com Sucesso!")
    msgBox.setWindowTitle("Aviso!!!")
    return msgBox.exec()

def limpaTela():
    tela.tituloTxt.setText("")
    tela.verSistemaTxt.setText("")
    tela.verModuloTxt.setText("")
    tela.problemaTxt.setPlainText("")
    tela.resolucaoTxt.setPlainText("")
    telaCadastraSistema.dsSystem.setText("")
    telaCadastraModulo.dsModulo.setText("")
    tela.boxSistema.clear()
    consultaSistema = list(map(str, dbPost.consulta_db("SELECT nmsistema FROM gerenciador.system ORDER BY nmsistema")))
    dbPost.removeCarac(consultaSistema)
    sistema = dbPost.removeCarac(consultaSistema)
    tela.boxSistema.addItems(sistema)
    tela.checkDuvida.setChecked(True)
    telaProcesso.cdProcesso.setText("")
    tela.checkProcesso.setChecked(False)
    tela.show()

def cadastraSistema():
    newSistema = telaCadastraSistema.dsSystem.text().upper()
    insertSistema = dbPost.insert_db("INSERT INTO gerenciador.system (nmsistema) VALUES ('" + newSistema + "');")
    telaCadastraSistema.close()
    telaCadastraSistema.dsSystem.setText("")
    tela.close()
    consultaSistema = list(map(str, dbPost.consulta_db("SELECT nmsistema FROM gerenciador.system ORDER BY nmsistema")))
    dbPost.removeCarac(consultaSistema)
    sistema = dbPost.removeCarac(consultaSistema)
    tela.boxSistema.clear()
    tela.boxSistema.addItems(sistema)
    tela.show()

def cadastraModulo():
    newModulo = telaCadastraModulo.dsModulo.text()
    insertModulo = dbPost.insert_db("INSERT INTO gerenciador.module (dsmodulo) VALUES ('" + newModulo+ "');")
    telaCadastraModulo.close()
    telaCadastraModulo.dsModulo.setText("")
    tela.close()
    consultaModulo = list(map(str, dbPost.consulta_db("SELECT dsmodulo FROM gerenciador.module ORDER BY dsmodulo")))
    dbPost.removeCarac(consultaModulo)
    modulo = dbPost.removeCarac(consultaModulo)
    tela.boxModulo.clear()
    tela.boxModulo.addItems(modulo)
    tela.show()

def persistirDica(dica:Dica):
    dica = Dica
    dica.processo = telaProcesso.cdProcesso.text()
    insert = dbPost.insert_db("INSERT INTO gerenciador.gerenciador "
                              "(titulo, dt_dica, sistema, versao_sistema, modulo, "
                              "versao_modulo, problema, resolucao, st_problema, comentario, processo, st_resolvido) VALUES ('" + dica.titulo +
                              "', '" + dica.data + "', '" + dica.sistema + "', '" + dica.verSistema +
                              "', '" + dica.modulo + "', '" + dica.verModulo + "', '" + dica.problema +
                              "', '" + dica.resolucao + "', '" + dica.tipoDuvida + "', '', '" + dica.processo + "', False);")
    limpaTela()
    telaProcesso.close()
    msgSucesso()


def enviaProcesso(dica:Dica):
    if tela.checkProcesso.isChecked() or dica.tipoDuvida == "True":
        telaProcesso.show()
    else:
        persistirDica(Dica)


def enviaDica():
    dica = Dica
    dica.titulo = tela.tituloTxt.text().upper()
    dica.data = datetime.date.today().strftime('%d/%m/%Y')
    dica.sistema = tela.boxSistema.currentText()
    dica.verSistema = tela.verSistemaTxt.text()
    dica.modulo = tela.boxModulo.currentText()
    dica.verModulo = tela.verModuloTxt.text()
    dica.problema = tela.problemaTxt.toPlainText()
    dica.resolucao = tela.resolucaoTxt.toPlainText()

    if tela.checkDuvida.isChecked() == True:
        dica.tipoDuvida = str(False)
    else:
        dica.tipoDuvida = str(True)

    if dica.verificaDica(dica) == False:
        msgCampos()

    else:
        enviaProcesso(dica)




app = QtWidgets.QApplication([])

tela = uic.loadUi("Gerencia Dica.ui")
telaCadastraModulo = uic.loadUi("CadastraModulo.ui")
telaCadastraSistema = uic.loadUi("CadastraSistema.ui")
telaProcesso = uic.loadUi("EnviaProcesso.ui")


consultaSistema = list(map(str, dbPost.consulta_db("SELECT nmsistema FROM gerenciador.system ORDER BY nmsistema")))
dbPost.removeCarac(consultaSistema)
sistema = dbPost.removeCarac(consultaSistema)
tela.boxSistema.addItems(sistema)

consultaModulo = list(map(str, dbPost.consulta_db("SELECT dsmodulo FROM gerenciador.module ORDER BY dsmodulo")))
dbPost.removeCarac(consultaModulo)
modulo = dbPost.removeCarac(consultaModulo)
tela.boxModulo.addItems(modulo)

tela.enviar.clicked.connect(enviaDica)

tela.adicionaSistema.clicked.connect(telaCadastraSistema.show)
tela.adicionaMod.clicked.connect(telaCadastraModulo.show)

telaCadastraSistema.cadastraSistema.clicked.connect(cadastraSistema)
telaCadastraModulo.cadastraModulo.clicked.connect(cadastraModulo)

telaProcesso.enviaProcesso.clicked.connect(persistirDica)

tela.show()
app.exec()

