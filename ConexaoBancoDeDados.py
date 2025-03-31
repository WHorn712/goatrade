

from datetime import datetime
import pytz
import pyodbc


def conectar_BD(im):
    """Conexão com banco de dados"""
    timezone = pytz.timezone("Etc/UTC")

    utc_from = datetime(2024, 1, 15, hour=11, minute=50, tzinfo=timezone)
    dados_conexao = (
        "Driver={SQL Server};"
        "Server=DESKTOP-VDQPO57\SQLEXPRESS;"
        "Database=movesgoat"
    )
    conexao = pyodbc.connect(dados_conexao)
    print('banco de dados atualizado')