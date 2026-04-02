import psycopg2
import random
from faker import Faker
from datetime import date, timedelta

fake = Faker("pt_BR")

DB_CONFIG = {
    "host": "localhost",
    "database": "rh_db",
    "user": "luizotavio",
    "password": "senha123"
}

DEPARTAMENTOS = [
    "Tecnologia", "Financeiro", "Comercial",
    "Recursos Humanos", "Marketing", "Operações"
]

CARGOS = {
    "Tecnologia":       ["Desenvolvedor Júnior", "Desenvolvedor Pleno", "Analista de Dados", "DevOps"],
    "Financeiro":       ["Analista Financeiro", "Contador", "Auxiliar Financeiro"],
    "Comercial":        ["Vendedor", "Gerente Comercial", "SDR"],
    "Recursos Humanos": ["Analista de RH", "Recrutador", "HRBP"],
    "Marketing":        ["Analista de Marketing", "Designer", "Social Media"],
    "Operações":        ["Analista de Operações", "Supervisor", "Coordenador"]
}

SALARIOS = {
    "Desenvolvedor Júnior":  (3500, 5000),
    "Desenvolvedor Pleno":   (6000, 9000),
    "Analista de Dados":     (4000, 7000),
    "DevOps":                (7000, 11000),
    "Analista Financeiro":   (3500, 6000),
    "Contador":              (4000, 7000),
    "Auxiliar Financeiro":   (2000, 3500),
    "Vendedor":              (2500, 4000),
    "Gerente Comercial":     (8000, 14000),
    "SDR":                   (2500, 3500),
    "Analista de RH":        (3000, 5000),
    "Recrutador":            (3000, 4500),
    "HRBP":                  (5000, 8000),
    "Analista de Marketing": (3000, 5000),
    "Designer":              (3000, 5000),
    "Social Media":          (2500, 4000),
    "Analista de Operações": (3000, 5000),
    "Supervisor":            (5000, 8000),
    "Coordenador":           (6000, 10000)
}

def resetar_banco():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE funcionarios RESTART IDENTITY CASCADE")
    cursor.execute("TRUNCATE TABLE departamentos RESTART IDENTITY CASCADE")
    cursor.close()
    conn.close()
    print("Banco resetado.")

def criar_tabelas():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departamentos (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            cargo TEXT NOT NULL,
            departamento_id INTEGER REFERENCES departamentos(id),
            salario NUMERIC(10,2) NOT NULL,
            data_contratacao DATE NOT NULL,
            data_desligamento DATE,
            ativo BOOLEAN DEFAULT TRUE
        )
    """)
    cursor.close()
    conn.close()
    print("Tabelas verificadas.")

def popular_dados():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()

    dept_ids = {}
    for dept in DEPARTAMENTOS:
        cursor.execute(
            "INSERT INTO departamentos (nome) VALUES (%s) RETURNING id",
            (dept,)
        )
        dept_ids[dept] = cursor.fetchone()[0]

    print(f"Departamentos inseridos: {dept_ids}")

    for i in range(200):
        dept = random.choice(DEPARTAMENTOS)
        cargo = random.choice(CARGOS[dept])
        sal_min, sal_max = SALARIOS[cargo]
        salario = round(random.uniform(sal_min, sal_max), 2)

        data_contratacao = fake.date_between(
            start_date=date(2018, 1, 1),
            end_date=date(2024, 12, 31)
        )

        ativo = random.random() > 0.2
        data_desligamento = None
        if not ativo:
            dias = random.randint(90, 1000)
            data_desligamento = data_contratacao + timedelta(days=dias)
            if data_desligamento > date.today():
                data_desligamento = date.today()

        cursor.execute("""
            INSERT INTO funcionarios
                (nome, email, cargo, departamento_id, salario,
                 data_contratacao, data_desligamento, ativo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            fake.name(),
            fake.email(),
            cargo,
            dept_ids[dept],
            salario,
            data_contratacao,
            data_desligamento,
            ativo
        ))

        if (i + 1) % 50 == 0:
            print(f"{i + 1} funcionários inseridos...")

    cursor.close()
    conn.close()
    print("200 funcionários gerados com sucesso.")

if __name__ == "__main__":
    criar_tabelas()
    resetar_banco()
    popular_dados()