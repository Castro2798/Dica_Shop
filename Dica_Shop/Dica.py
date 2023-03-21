
class Dica:
    titulo = str
    data = str
    sistema = str
    verSistema = str
    modulo = str
    verModulo = str
    tipoDuvida = str
    problema = str
    resolucao = str
    comentario = str
    processo = str
    stResolvido = str
def verificaDica(dica:Dica):
    if dica.titulo == '' or dica.problema == '' or dica.resolucao == '':
        return False
    else:
        return True
