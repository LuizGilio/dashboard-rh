# Dashboard de RH — Análise de Pessoas

Dashboard interativo de Recursos Humanos construído com Power BI, conectado a um banco PostgreSQL com dados gerados via Python.

## Tecnologias

- Python 3.12
- PostgreSQL
- SQLAlchemy
- Pandas
- Power BI Desktop
- Faker (geração de dados realistas)

## Funcionalidades

- KPIs: total de funcionários e ativos
- Headcount por departamento
- Contratações por ano (2018–2024)
- Salário médio por cargo
- Top 3 salários por departamento
- Filtro interativo por departamento

## SQL Avançado utilizado

- LEFT JOIN entre departamentos e funcionários
- COUNT com FILTER para ativos e desligados
- AVG, MIN, MAX para análise salarial
- RANK() OVER PARTITION BY — window function de ranking
- EXTRACT e COALESCE para cálculo de tempo na empresa
- GROUP BY com múltiplas agregações

## Como rodar

Clone o repositório:
```bash
git clone https://github.com/LuizGilio/dashboard-rh.git
cd dashboard-rh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Configure o PostgreSQL e crie o banco:
```bash
sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE rh_db OWNER luizotavio;"
```

Gere os dados:
```bash
python3 gerar_dados.py
```

Exporte os CSVs:
```bash
python3 exportar.py
```

Abra o arquivo `dashboard-rh.pbix` no Power BI Desktop e atualize o caminho dos CSVs.

## Aprendizados

- SQL avançado com JOINs, window functions e agregações
- Geração de dados realistas com Faker
- Exportação de dados para CSV com encoding correto
- Criação de dashboard interativo no Power BI
- Segmentação de dados com filtros cruzados