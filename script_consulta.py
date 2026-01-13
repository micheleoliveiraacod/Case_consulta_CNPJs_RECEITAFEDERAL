# Script para consultar CNPJs em massa e preencher uma planilha Excel

import re  #trabalha com expressões regulares (re.sub(r"\D", "", cnpj))
import time #serve para respeitar o limite de requisições da API e evita bloqueios
import requests #Faz requisições HTTP para APIs de CNPJ e recebe as respostas em JSON.
import pandas as pd #le e manipula os dados
from openpyxl import load_workbook #le e manipula os dados
from datetime import datetime #registra data e hora

ARQUIVO = "consulta_cnpj.xlsx"
PLANILHA = "Planilha1"

# Função para limpar CNPJ (tira pontos, barra e hífen)
def limpar_cnpj(cnpj_str: str) -> str:
    if pd.isna(cnpj_str):
        return ""
    return re.sub(r"\D", "", str(cnpj_str))

# Função que consulta a API ReceitaWS (melhor para dados completos)
def consultar_cnpj_receitaws(cnpj_limpo: str) -> dict:
    """
    Consulta ReceitaWS - API gratuita com dados completos
    Limite: 3 requisições por minuto (respeita com sleep)
    """
    url = f"https://receitaws.com.br/v1/cnpj/{cnpj_limpo}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"  ⚠️ Erro na requisição: {e}")
    return {}

# Função alternativa: BrasilAPI (mais rápida, menos campos, traz os socios)
def consultar_cnpj_brasilapi(cnpj_limpo: str) -> dict:
    """
    Consulta BrasilAPI - API experimental, pode ter limites maiores
    """
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"  ⚠️ Erro na requisição: {e}")
    return {}

# Mapeia o JSON da API para as colunas da sua planilha
def extrair_campos(dados: dict, origem: str = "receitaws") -> dict:
    """
    Extrai e mapeia os dados da API para as colunas do Excel
    """
    if not dados:
        return {
            "SITUAÇÃO CADASTRAL": "",
            "ESTADO": "",
            "CIDADE": "",
            "NATUREZA JURIDICA": "",
            "PORTE": "",
            "CNAE": "",
            "ENDEREÇO": "",
            "E-MAIL": "",
            "TELEFONE": "",
            "SOCIOS": "",
        }

    if origem == "receitaws":
        # Mapeamento ReceitaWS
        endereco = f"{dados.get('logradouro', '')} {dados.get('numero', '')} {dados.get('bairro', '')} - {dados.get('cep', '')}"
        
        # Sócios (ReceitaWS não retorna, mas poderia)
        socios = dados.get('qsa', [])
        socios_str = "; ".join([s.get('nome', '') for s in socios if s.get('nome')])

        return {
            "SITUAÇÃO CADASTRAL": dados.get("situacao", ""),
            "ESTADO": dados.get("uf", ""),
            "CIDADE": dados.get("municipio", ""),
            "NATUREZA JURIDICA": dados.get("natureza_juridica", ""),
            "PORTE": dados.get("porte", ""),
            "CNAE": dados.get("cnae_fiscal", dados.get("atividade_principal", [{}])[0].get("code", "")),
            "ENDEREÇO": endereco.strip(),
            "E-MAIL": dados.get("email", ""),
            "TELEFONE": dados.get("telefone", ""),
            "SOCIOS": socios_str,
        }
    
    else:  # brasilapi
        # Mapeamento BrasilAPI
        endereco = f"{dados.get('logradouro', '')} {dados.get('numero', '')} {dados.get('bairro', '')} - {dados.get('cep', '')}"
        
        socios = dados.get('qsa', [])
        socios_str = "; ".join([s.get('nome_socio', '') for s in socios if s.get('nome_socio')])

        return {
            "SITUAÇÃO CADASTRAL": dados.get("descricao_situacao_cadastral", ""),
            "ESTADO": dados.get("uf", ""),
            "CIDADE": dados.get("municipio", ""),
            "NATUREZA JURIDICA": dados.get("natureza_juridica", ""),
            "PORTE": dados.get("porte", ""),
            "CNAE": dados.get("cnae_fiscal", ""),
            "ENDEREÇO": endereco.strip(),
            "E-MAIL": dados.get("email", ""),
            "TELEFONE": dados.get("ddd_telefone_1", ""),
            "SOCIOS": socios_str,
        }

def processar_planilha():
    """
    Lê o Excel, consulta cada CNPJ e preenche as colunas C até L
    """
    print(f"📂 Carregando arquivo: {ARQUIVO}")
    df = pd.read_excel(ARQUIVO, sheet_name=PLANILHA)

    print(f"📊 Total de CNPJs a consultar: {len(df)}\n")

    # Garante que as colunas de destino existem
    colunas_destino = [
        "SITUAÇÃO CADASTRAL",
        "ESTADO",
        "CIDADE",
        "NATUREZA JURIDICA",
        "PORTE",
        "CNAE",
        "ENDEREÇO",
        "E-MAIL",
        "TELEFONE",
        "SOCIOS",
    ]
    for col in colunas_destino:
        if col not in df.columns:
            df[col] = ""

    # Processa cada linha
    for idx, row in df.iterrows():
        cnpj_raw = row["CNPJ"]
        cnpj_limpo = limpar_cnpj(cnpj_raw)
        
        if not cnpj_limpo:
            print(f"❌ Linha {idx + 2}: CNPJ vazio ou inválido")
            continue

        print(f"🔍 [{idx + 1}/{len(df)}] Consultando CNPJ: {cnpj_raw}")
        
        # Tenta ReceitaWS primeiro (mais completo)
        dados = consultar_cnpj_receitaws(cnpj_limpo)
        origem = "receitaws"
        
        # Se falhar, tenta BrasilAPI
        if not dados or dados.get("status") == "ERROR":
            print(f"  ↪️ Tentando BrasilAPI...")
            dados = consultar_cnpj_brasilapi(cnpj_limpo)
            origem = "brasilapi"

        campos = extrair_campos(dados, origem)

        for col, valor in campos.items():
            df.at[idx, col] = valor

        if dados:
            print(f"  ✅ Dados preenchidos ({origem})")
        else:
            print(f"  ⚠️ Nenhum dado encontrado")

        # Respeita limite de requisições (3 por minuto = 20 seg entre requisições)
        time.sleep(21)

    # Salva de volta no Excel
    print(f"\n Salvando arquivo: {ARQUIVO}")
    with pd.ExcelWriter(ARQUIVO, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=PLANILHA, index=False)

    print("Processo concluído!")

if __name__ == "__main__":
    print("=" * 60)
    print("   AUTOMAÇÃO DE CONSULTA DE CNPJ - ATUALIZAÇÃO EXCEL")
    print("=" * 60)
    processar_planilha()