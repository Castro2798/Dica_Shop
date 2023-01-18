import psycopg2

class dbPost():

    novaLista = []

    def connect_db():
        with open('Connect.ini', 'r') as arquivo:
            connect = arquivo.read().split()
        host = connect[1]
        db = connect[2]
        user = connect[3]
        password = connect[4]
        conecta = psycopg2.connect(host=host[5::],
                                   database=db[9::],
                                   user=user[9::],
                                   password=password[9::])
        return conecta

    def consulta_db(sql):
        con = dbPost.connect_db()
        cur = con.cursor()
        cur.execute(sql)
        recset = cur.fetchall()
        registros = []
        for rec in recset:
            registros.append(rec)
        con.close()
        return registros

    def insert_db(sql):
        con = dbPost.connect_db()
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

    def removeCarac(c):
        novaLista = []
        l = 0
        while True:
            if l < len(c):
                removerCarac = c[l]
                removerCarac2 = removerCarac.replace("(", "")
                removerCarac3 = removerCarac2.replace("'", "")
                removerCarac4 = removerCarac3.replace(",", "")
                removerCarac5 = removerCarac4.replace(")", "")
                novaLista.append(removerCarac5)
                l += 1
            else:
                return novaLista
