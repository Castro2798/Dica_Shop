from pychartjs import BaseChart, ChartType, Color
import psycopg2 as pg
import jinja2
import os
from pathlib import Path

from consultas import ConsultaPagamento,ConsultaProdVendido

TPREC=[]
VLRECEBIDO=[]

PROD=[]
VLITEM=[]

class MyBarGraph(BaseChart):
    type = ChartType.HorizontalBar

    class labels:
        group = TPREC

    class data:
        label = "Valor Recebido"
        data = VLRECEBIDO

        fill = False
        pointBorderWidth = 10
        pointRadius = 3
        backgroundColor = Color.Green

with open(r'C:\ProgramData\Dash\Connect.ini', 'r') as arquivo:
    Connect=arquivo.read().split()
host=Connect[1]
db=Connect[2]
user=Connect[3]
password=Connect[4]

def conecta():
    con = pg.connect(host=host[5::],
                     database=db[9::],
                     user=user[9::],
                     password=password[9::])
    cur = con.cursor()
    sql = ConsultaPagamento()
    cur.execute(sql.getConPag())
    print(sql.getConPag())
    con.commit()
    recset = cur.fetchall()
    con.close()
    x=0
    for t in recset:
        TPREC.insert(x,t[0])
        VLRECEBIDO.insert(x,t[1])
        x=x+1
    iniciaDash()

def iniciaDash():
    chart = MyBarGraph()
    dir = os.path.dirname(os.path.abspath(__file__))
    template = os.path.join(dir, 'template')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template))
    html = env.get_template('template.html')
    page = os.path.join(dir, 'html', 'template.html')
    renderedPag = html.render(title='Dash Spice', chartPag=chart.get())
    outputFileName = Path('template/index.html')
    with open(outputFileName, 'w') as outputFile:
        outputFile.write(renderedPag)

conecta()

