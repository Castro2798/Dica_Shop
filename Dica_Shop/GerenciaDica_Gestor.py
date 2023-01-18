import datetime
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from dbPost import dbPost
import pandas as pd
import Dica


LISTA = ""
date =  pd.to_datetime("today")
DT_INICIAL = pd.Period(date, freq= 'M').start_time.date().strftime('%d/%m/%Y')
DT_FINAL = pd.Period(date, freq= 'M').end_time.date().strftime('%d/%m/%Y')

def filtraDica():
    DT_INICIAL = tela.dtInicial.selectedDate().strftime('%d/%m/%Y')
    DT_FINAL = tela.dtFinal.selectedDate().strftime('%d/%m/%Y')
    print(DT_FINAL)


def listarDados():
    global LISTA, DT_FINAL, DT_FINAL
    print(DT_FINAL)
    print(DT_INICIAL)
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
    tela.tableWidget.setRowCount(0)
    for linha, dados in enumerate(LISTA):
        tela.tableWidget.insertRow(linha)
        for coluna, dados in enumerate(dados):
            tela.tableWidget.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados)))

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

def comentaDica():
    comentario = tela.comentario.toPlainText()
    codigo = LISTA[int(tela.tableWidget.currentRow())][0]
    codigoStr = str(codigo)
    enviaComentario = dbPost.insert_db("UPDATE gerenciador.gerenciador SET comentario = '" + comentario + "' WHERE codigo = " + codigoStr)
    tela.close()
    listarDados()
    tela.show()

app=QtWidgets.QApplication([])
tela = uic.loadUi("GerenciaDica_Gestor.ui")

tela.comentar.clicked.connect(comentaDica)


listarDados()
app.exec()