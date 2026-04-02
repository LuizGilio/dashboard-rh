import pandas as pd
from sqlalchemy import create_engine

ENGINE = create_engine(
    "postgresql://luizotavio:senha123@localhost/rh_db"
)

def headcount_por_departamento():
    query = """
        SELECT 
            d.nome AS departamento,
            COUNT(f.id) AS total_funcionarios,
            COUNT(f.id) FILTER (WHERE f.ativo = TRUE) AS ativos,
            COUNT(f.id) FILTER (WHERE f.ativo = FALSE) AS desligados
        FROM departamentos d
        LEFT JOIN funcionarios f ON f.departamento_id = d.id
        GROUP BY d.nome
        ORDER BY total_funcionarios DESC
    """
    return pd.read_sql(query, ENGINE)

def salario_medio_por_cargo():
    query = """
        SELECT
            cargo,
            COUNT(*) AS total,
            ROUND(AVG(salario), 2) AS salario_medio,
            ROUND(MIN(salario), 2) AS salario_minimo,
            ROUND(MAX(salario), 2) AS salario_maximo
        FROM funcionarios
        WHERE ativo = TRUE
        GROUP BY cargo
        ORDER BY salario_medio DESC
    """
    return pd.read_sql(query, ENGINE)

def contratacoes_por_ano():
    query = """
        SELECT
            EXTRACT(YEAR FROM data_contratacao)::INT AS ano,
            COUNT(*) AS contratacoes
        FROM funcionarios
        GROUP BY ano
        ORDER BY ano
    """
    return pd.read_sql(query, ENGINE)

def ranking_salario_por_departamento():
    query = """
        SELECT
            f.nome,
            d.nome AS departamento,
            f.cargo,
            f.salario,
            RANK() OVER (
                PARTITION BY d.nome
                ORDER BY f.salario DESC
            ) AS ranking_no_depto
        FROM funcionarios f
        JOIN departamentos d ON f.departamento_id = d.id
        WHERE f.ativo = TRUE
        ORDER BY d.nome, ranking_no_depto
    """
    return pd.read_sql(query, ENGINE)

def tempo_medio_empresa():
    query = """
        SELECT
            d.nome AS departamento,
            ROUND(
                AVG(
                    (COALESCE(f.data_desligamento, CURRENT_DATE) - f.data_contratacao)
                ) / 365.0, 1
            ) AS tempo_medio_anos
        FROM funcionarios f
        JOIN departamentos d ON f.departamento_id = d.id
        GROUP BY d.nome
        ORDER BY tempo_medio_anos DESC
    """
    return pd.read_sql(query, ENGINE)

if __name__ == "__main__":
    print("\n--- Headcount por Departamento ---")
    print(headcount_por_departamento().to_string(index=False))

    print("\n--- Salário Médio por Cargo (Top 5) ---")
    print(salario_medio_por_cargo().head().to_string(index=False))

    print("\n--- Contratações por Ano ---")
    print(contratacoes_por_ano().to_string(index=False))

    print("\n--- Top 3 Salários por Departamento ---")
    df = ranking_salario_por_departamento()
    print(df[df["ranking_no_depto"] <= 3].to_string(index=False))

    print("\n--- Tempo Médio na Empresa por Departamento ---")
    print(tempo_medio_empresa().to_string(index=False))