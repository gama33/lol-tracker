import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import init_db, drop_all_tables, check_db_connection, reset_database, get_db_info

def main():
    if len(sys.argv) < 2:
        print_help()
        return

    comando = sys.argv[1].lower()

    if comando == "init":
        cmd_init()
    elif comando == "drop":
        cmd_drop()
    elif comando == "reset":
        cmd_reset()
    elif comando == "check":
        cmd_check()
    elif comando == "info":
        cmd_info()
    else:
        print(f"Comando desconhecida: {comando}\n")
        print_help()

def print_help():
    print("""
Gerenciador de Banco de Dados - LOL Tracker

Uso: python -m backend.db_utils <comando>

Comandos disponíveis:

  init      Cria todas as tabelas no banco de dados
  drop      Remove todas as tabelas (cuidado!)
  reset     Remove e recria todas as tabelas
  check     Verifica se a conexão com o banco está funcionando
  info      Exibe informações sobre a configuração do banco

Exemplos:
  python -m backend.db_utils init
""")

def cmd_init():
    print("\n ESSE COMANDO IRÁ APAGAR TODAS AS TABELAS!\n")
    confirmacao = input("Digite 'SIM' para confirmar: ")

    if confirmacao != "SIM":
        print("\n Operação cancelada.\n")
        return

    print("\n Removendo todas as tabelas... \n")
    try:
        drop_all_tables()
        print("\n Tabelas removidas com sucesso!\n")
    except Exception as e:
        print(f"\n Erro ao remover tabelas: {e}")
        sys.exit(1)

def cmd_reset():
    print("\n ATENÇÃO: Essa ação irá RESETAR o banco de dados")
    confirmacao = input("Digite 'SIM' para confirmar:")

    if confirmacao != "SIM":
        print("\n Operação cancelada.\n")
        return
    
    print("\n Resetando bando de dados...\n")
    try:
        reset_database()
        print("\nBanco de dados resetado com sucesso!\n")
    except Exception as e:
        print(f"Erro ao resetar banco: {e}")
        sys.exit(1)

def cmd_check():
    print("\n Verificando conexão com banco de dados...\n")

    if check_db_connection():
        print("Conexão estabelecida com sucesso!\n")
    else:
        print("Falha na conexão com banco de dados!\n")
        sys.exit(1)
    
def cmd_info():
    print("\n Informações do Banco de Dados:\n")

    try:
        info = get_db_info()
        print(f"  Database URL: {info['database_url']}")
        print(f"  Pool Size: {info['pool_size']}")
        print(f"  Max Overflow: {info['max_overflow']}")
        print(f"  SQL Echo: {info['echo']}")
        print()
    except Exception as e:
        print(f"Erro ao obter informações: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
