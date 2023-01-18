
class QuerySql:

    def __init__(self,sql=""):
        self.sql = sql

    def setSql(self, newSql):
        self.sql=newSql

    def getSql(self):
        return self.sql