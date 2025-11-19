from sqlalchemy import create_engine, text
from openpyxl import Workbook

# --- CONFIGURE YOUR DATABASE CONNECTION HERE ---
# Example for PostgreSQL:
# engine = create_engine('postgresql://user:password@host:port/database')
engine = create_engine('sqlite:///example.db')  # Placeholder, replace with your DB

# --- SQL QUERY WITH PARAMETER ---
SQL_QUERY = """
WITH pagamentos_filtrados AS (
    SELECT 
        pag_pk_pagamento,
        pag_fk_parcela,
        pag_dd_pagamento,
        pag_vl_pago,
        pag_tx_pagamento_tipo
    FROM credit_portfolio.pagamento
    WHERE pag_dd_pagamento = :data_inicio
),
metrica_agregada AS (
    SELECT 
        mtr_fk_contrato,
        SUM(mtr_VL_presente) as total_valor_presente
    FROM credit_portfolio.metrica
    WHERE mtr_dd_data = :data_inicio
    GROUP BY mtr_fk_contrato
),
cedentes AS (
    SELECT DISTINCT 
        pte_nr_cpf_cnpj,
        pte_tx_nome
    FROM credit_portfolio.participante
    WHERE left(pte_pk_participante,3) = 'ced'
),
sacados AS (
    SELECT DISTINCT 
        pte_nr_cpf_cnpj,
        pte_tx_nome
    FROM credit_portfolio.participante
    WHERE left(pte_pk_participante,3) = 'sac'
)
SELECT con.con_tx_fundo_nome as fundo_nome,
       con.con_nr_fundo_cnpj as fundo_cnpj,
       pag.pag_dd_pagamento,
       ced.pte_tx_nome as cedente_nome,
       con.con_nr_cedente_cpf_cnpj as cedente_numero_documento,
       sac.pte_tx_nome as sacado_nome,
       con.con_nr_sacado_cpf_cnpj as sacado_numero_documento,
       con.con_vl_taxa_pre,
       con.con_dd_aquisicao as contrato_data_cessao,
       par.par_dd_vencimento_ajustado as parcela_data_vencimento_ajustada,
       par.par_vl_aquisicao,
       par.par_vl_nominal_original,
       con.con_tx_produto_nome as produto_nome,
       con.con_tx_recebivel_tipo as contrato_tipo_recebivel,
       con.con_nr_coobrigacao,
       con.con_pk_contrato as __Contrato__,
       par.par_pk_parcela as __Parcela__,
       par.par_nr_parcela as Nr_Parcela,
       pag.pag_vl_pago as pag_vl_pago,
       pag.pag_tx_pagamento_tipo,
       mtr.total_valor_presente
FROM pagamentos_filtrados as pag
INNER JOIN credit_portfolio.parcela as par 
    ON pag.pag_fk_parcela = par.par_pk_parcela
INNER JOIN credit_portfolio.contrato as con 
    ON par.par_fk_contrato = con.con_pk_contrato
LEFT JOIN metrica_agregada mtr 
    ON con.con_pk_contrato = mtr.mtr_fk_contrato
LEFT JOIN cedentes ced
    ON con.con_nr_cedente_cpf_cnpj = ced.pte_nr_cpf_cnpj
LEFT JOIN sacados sac
    ON con.con_nr_sacado_cpf_cnpj = sac.pte_nr_cpf_cnpj
WHERE con.con_tx_fundo_nome IN (
      'VECTOR EDGE FUNDO DE INVESTIMENTO EM DIREITOS CREDITORIOS',
      'MERCADO CRÉDITO FUNDO DE INVESTIMENTO EM DIREITOS CREDITÓRIOS NÃO PADRONIZADO',
      'MÉLIUZ FUNDO DE INVESTIMENTO EM DIREITOS CREDITÓRIOS',
      'VLTZ I FUNDO DE INVESTIMENTO EM DIREITOS CREDITÓRIOS NÃO PADRONIZADO',
      'PLGN FORNECEDORES FUNDO DE INVESTIMENTO EM DIREITOS CREDITÓRIOS'
  )
ORDER BY pag.pag_dd_pagamento;
"""



from datetime import datetime, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def main():
    # List of dates to process
    date_list = [
        "2025-11-03","2025-11-04",
        "2025-11-05","2025-11-06",
        "2025-11-07",
        "2025-11-10","2025-11-11","2025-11-12","2025-11-13","2025-11-14",
        "2025-11-17","2025-11-18",
        "2025-11-19"
    ]

    with engine.connect() as conn:
        for date_str in date_list:
            result = conn.execute(text(SQL_QUERY), {"data_inicio": date_str})
            columns = result.keys()
            rows = result.fetchall()

            wb = Workbook()
            ws = wb.active
            ws.append(list(columns))
            for row in rows:
                ws.append(list(row))
            filename = f"output_{date_str}.xlsx"
            wb.save(filename)
            print(f"Exported results to {filename}")

if __name__ == "__main__":
    main()
