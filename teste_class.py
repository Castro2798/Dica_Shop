t = 'SELECT rec.dstprec AS pagamento, '\
                                         'sum(mc.vl_valor) AS valor '\
                                         'FROM spice.movimento_caixa AS mc '\
                                         'INNER JOIN spice.tprec AS rec '\
                                         'ON mc.id_tipo_recebimento = rec.idtprec '\
                                         'GROUP BY idtprec '\
                                         'ORDER BY valor'
print(t)