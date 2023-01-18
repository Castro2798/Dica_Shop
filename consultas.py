
class ConsultaPagamento:

    filtraPag = 'SELECT rec.dstprec AS pagamento, ' \
                                  'sum(mc.vl_valor) AS valor ' \
                                  'FROM spice.movimento_caixa AS mc ' \
                                  'INNER JOIN spice.tprec AS rec ' \
                                  'ON mc.id_tipo_recebimento = rec.idtprec ' \
                                  'GROUP BY idtprec ' \
                                  'ORDER BY valor'

    def __init__(self, conPag=filtraPag):
        self.conPag = conPag

    def getConPag(self):
        return self.conPag


class ConsultaProdVendido:

    filtraProdVendido = 'SELECT p.dsproduto, ' \
                                     'sum(mi.qtdeproduto), ' \
                                     'sum(mi.vltotal) ' \
                                     'FROM spice.movimentoitem ' \
                                     'AS mi INNER JOIN spice.produtos AS p ' \
                                     'ON mi.idproduto = p.idproduto ' \
                                     'GROUP BY dsproduto'

    def __init__(self, conProd=filtraProdVendido):
        self.conProd=conProd

    def getConProd(self):
        return self.conProd
