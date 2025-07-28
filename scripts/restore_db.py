import os
import subprocess

# Caminho para o arquivo SQL
dump_file = os.path.join(os.path.dirname(__file__), "bayala_dump.sql")

# Constrói o comando psql a partir das variáveis de ambiente
db_name = os.getenv("DB_NAME", "bayala_db")
db_user = os.getenv("DB_USER", "bayala_db_user")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_password = os.getenv("DB_PASSWORD", "Desportivo")

# Exporta a senha como variável de ambiente
os.environ["PGPASSWORD"] = db_password

# Comando psql
command = [
    "psql",
    "-h", db_host,
    "-U", db_user,
    "-d", db_name,
    "-p", db_port,
    "-f", dump_file,
]

print(f"Restaurando base de dados a partir de {dump_file}...")

try:
    subprocess.run(command, check=True)
    print("✅ Banco de dados restaurado com sucesso.")
except subprocess.CalledProcessError as e:
    print("❌ Erro ao restaurar banco:", e)
