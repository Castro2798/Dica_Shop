import os

caminho = "C:\ProgramData\Dash"

if os.path.lexists(caminho) == False:
    diretorioConnect = os.mkdir(r"C:\ProgramData\Dash")
else:
    host = input(str('Host='))
    db = input(str('Database='))
    user = input(str('Username='))
    password = input(str('Password='))

    arquivoText = "[CONNECT]\nHost="+host+"\nDatabase="+db+"\nUsername="+user+"\nPassword="+password

    if os.path.lexists(caminho + "\Connect.ini") == False:
        arquivoConnect = open('C:/ProgramData/Dash/Connect.ini', 'a')
        arquivoConnect.writelines(arquivoText)
    else:
        print("Concluído!")