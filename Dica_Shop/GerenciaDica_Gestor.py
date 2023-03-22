from PyQt5 import uic, QtWidgets
from dbPost import dbPost
import pandas as pd


date =  pd.to_datetime("today")
DT_INICIAL = pd.Period(date, freq= 'M').start_time.date().strftime('%d/%m/%Y')
DT_FINAL = pd.Period(date, freq= 'M').end_time.date().strftime('%d/%m/%Y')
LISTA = dbPost.consulta_db("SELECT "
                               "codigo,"
                               "processo,"
                               "dt_dica,"
                               "titulo,"
                               "sistema,"
                               "versao_sistema,"
                               "modulo,"
                               "versao_modulo,"
                               "(CASE WHEN st_problema = False THEN 'Dúvida' ELSE 'Problema' END) AS tipo_duvida,"
                               "problema,"
                               "resolucao,"
                               "comentario "
                               "FROM gerenciador.gerenciador "
                               "WHERE dt_dica BETWEEN '" + DT_INICIAL + "' AND '" + DT_FINAL + "'ORDER BY dt_dica")
TIPO_DICA = ""
SISTEMAFILTRO = ""
def limpaDica():
    processo = tela.processo.setText("")
    titulo = tela.titulo.setText("")
    sistema = tela.sistema.setText("")
    verSistema = tela.verSistema.setText("")
    modulo = tela.modulo.setText("")
    verModulo = tela.verModulo.setText("")
    duvidaProblema = tela.duvidaProblema.setText("")
    resolucao = tela.resolucao.setText("")
    comentario = tela.comentario.setPlainText("")
    filtraDica()
    print("OI")
def filtraDica():
    global LISTA, DT_INICIAL, DT_FINAL, TIPO_DICA, SISTEMAFILTRO

    DT_INICIAL = tela.dtInicial.date().toPyDate().strftime("%Y-%m-%d")
    DT_FINAL = tela.dtFinal.date().toPyDate().strftime("%Y-%m-%d")
    duvidaCheck = tela.duvidaCheck.isChecked()
    problemaCheck = tela.problemaCheck.isChecked()
    SISTEMAFILTRO = tela.sistemaFiltro.text().upper()
    if duvidaCheck == True and problemaCheck == False:
        TIPO_DICA = "st_problema = False and "
        tela.close()
        listarDados()
    elif problemaCheck == True and duvidaCheck == False:
        TIPO_DICA = "st_problema = True and "
        tela.close()
        listarDados()
    else:
        TIPO_DICA = ""
        tela.close()
        listarDados()

def listarDados():
    global LISTA, DT_FINAL, DT_FINAL, TIPO_DICA, SISTEMAFILTRO

    if len(SISTEMAFILTRO) == 0:
        LISTA = dbPost.consulta_db("SELECT "
                                   "codigo,"
                                   "processo,"
                                   "dt_dica,"
                                   "titulo,"
                                   "sistema,"
                                   "versao_sistema,"
                                   "modulo,"
                                   "versao_modulo,"
                                   "(CASE WHEN st_problema = False THEN 'Dúvida' ELSE 'Problema' END) AS tipo_duvida,"
                                   "problema,"
                                   "resolucao,"
                                   "comentario,"
                                   "CAST(CASE WHEN st_resolvido=True THEN 'True' ELSE 'False' END AS varchar(5)) "
                                   "FROM gerenciador.gerenciador "
                                   "WHERE " + TIPO_DICA + " dt_dica BETWEEN '" + DT_INICIAL + "' AND '" + DT_FINAL + "' ORDER BY dt_dica")
        tela.tableWidget.setRowCount(0)
        for linha, dados in enumerate(LISTA):
            tela.tableWidget.insertRow(linha)
            for coluna, dados in enumerate(dados):
                tela.tableWidget.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados)))

        tela.checkBox.setChecked(True)
        tela.tableWidget.cellClicked.connect(atualizaView)

        tela.show()
    else:
        LISTA = dbPost.consulta_db("SELECT "
                                   "codigo,"
                                   "processo,"
                                   "dt_dica,"
                                   "titulo,"
                                   "sistema,"
                                   "versao_sistema,"
                                   "modulo,"
                                   "versao_modulo,"
                                   "(CASE WHEN st_problema = False THEN 'Dúvida' ELSE 'Problema' END) AS tipo_duvida,"
                                   "problema,"
                                   "resolucao,"
                                   "comentario,"
                                   "CAST(CASE WHEN st_resolvido=True THEN 'True' ELSE 'False' END AS varchar(5)) "
                                   "FROM gerenciador.gerenciador "
                                   "WHERE " + TIPO_DICA + " dt_dica BETWEEN '" + DT_INICIAL + "' AND '" + DT_FINAL + "' AND sistema ILIKE '%" + SISTEMAFILTRO + "%'ORDER BY dt_dica")

        tela.tableWidget.setRowCount(0)
        for linha, dados in enumerate(LISTA):
            tela.tableWidget.insertRow(linha)
            for coluna, dados in enumerate(dados):
                tela.tableWidget.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados)))

        tela.checkBox.setChecked(True)
        tela.tableWidget.cellClicked.connect(atualizaView)

        tela.show()

def atualizaView():
    processo = tela.processo.setText(LISTA[int(tela.tableWidget.currentRow())][1])
    titulo = tela.titulo.setText(LISTA[int(tela.tableWidget.currentRow())][3])
    sistema = tela.sistema.setText(LISTA[int(tela.tableWidget.currentRow())][4])
    verSistema = tela.verSistema.setText(LISTA[int(tela.tableWidget.currentRow())][5])
    modulo = tela.modulo.setText(LISTA[int(tela.tableWidget.currentRow())][6])
    verModulo = tela.verModulo.setText(LISTA[int(tela.tableWidget.currentRow())][7])
    duvidaProblema = tela.duvidaProblema.setText(LISTA[int(tela.tableWidget.currentRow())][9])
    resolucao = tela.resolucao.setText(LISTA[int(tela.tableWidget.currentRow())][10])
    comentario = tela.comentario.setPlainText(LISTA[int(tela.tableWidget.currentRow())][11])
    stResolvido = LISTA[int(tela.tableWidget.currentRow())][12]
    if stResolvido == "True":
        tela.checkBox.setChecked(True)
        tela.checkBox.setDisabled(True)
    else:
        tela.checkBox.setChecked(False)
        tela.checkBox.setDisabled(False)

def comentaDica():
    comentario = tela.comentario.toPlainText()
    codigo = LISTA[int(tela.tableWidget.currentRow())][0]
    codigoStr = str(codigo)
    resolvido = str(tela.checkBox.isChecked(True))
    enviaResolvido = dbPost.insert_db("UPDATE gerenciador.gerenciador SET st_resolvido = '" + resolvido + "' WHERE codigo = " + codigoStr)
    enviaComentario = dbPost.insert_db("UPDATE gerenciador.gerenciador SET comentario = '" + comentario + "' WHERE codigo = " + codigoStr)
    tela.close()
    listarDados()
    tela.show()

app=QtWidgets.QApplication([])
tela = uic.loadUi("GerenciaDica_Gestor.ui")

tela.dtInicial.setDate(pd.Period(date, freq= 'M').start_time.date())
tela.dtFinal.setDate(pd.Period(date, freq= 'M').end_time.date())

tela.comentar.clicked.connect(comentaDica)
tela.filtrar.clicked.connect(limpaDica)

listarDados()
app.exec()