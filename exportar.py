import pandas as pd
from sqlalchemy import create_engine
import os

ENGINE = create_engine(
    "postgresql://luizotavio:senha123@localhost/rh_db"
)

os.makedirs("dados_exportados", exist_ok=True)

queries = {
    "headcount": """
        SELECT
            d.nome AS departamento,
            COUNT(f.id) AS total_funcionarios,
            COUNT(f.id) FILTER (WHERE f.ativo = TRUE) AS ativos,
            COUNT(f.id) FILTER (WHERE f.ativo = FALSE) AS desligados
        FROM departamentos d
        LEFT JOIN funcionarios f ON f.departamento_id = d.id
        GROUP BY d.nome
        ORDER BY total_funcionarios DESC
    """,
    "salarios":"""
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
    """,
    "contratacoes":"""
        SELECT
            EXTRACT(YEAR FROM data_contratacao):: INT AS ano,
            COUNT(*) AS contratacoes
        FROM funcionarios
        GROUP BY ano
        ORDER BY ano
    """,
    "ranking":"""
        SELECT
            f.nome,
            d.nome AS departamento,
            f.cargo,
            f.salario,
            RANK() OVER(
                PARTITION BY d.nome
                ORDER BY f.salario DESC
            ) AS ranking_no_depto
        FROM funcionarios f
        JOIN departamentos d ON f.departamento_id  = d.id
        WHERE f.ativo = TRUE
        ORDER BY d.nome, ranking_no_depto
    """,
    "tempo_medio":"""
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
    """,
    "funcionarios_completo":"""
        SELECT
            f.id,
            f.nome,
            f.cargo,
            d.nome AS departamento,
            f.salario,
            f.data_contratacao,
            f.data_desligamento,
            f.ativo
        FROM funcionarios f
        JOIN departamentos d ON f.departamento_id = d.id
        ORDER BY f.id                    
    """
}

for nome, query in queries.items():
    df = pd.read_sql(query, ENGINE)
    caminho = f"dados_exportados/{nome}.csv"
    df.to_csv(caminho, index=False, encoding="utf-8-sig")
    print(f"Exportado: {caminho} ({len(df)} linhas)")

print ("\nTodos os arquivos exportados para a pasta dados_exportados/")    