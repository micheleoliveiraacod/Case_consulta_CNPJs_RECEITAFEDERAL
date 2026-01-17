# ⚙️ Consulta de CNPJ's na Receita Federal e Brasil API

## 📢 Sobre
Este codigo atualiza o cadastro de um dataset de clientes de uma empresa. Ele consulta por API, no site da Receita Federal e do BrasilAPI os dados das colunas em brando no excel , com base no numero do CNPJ's informados.

O uso indevido pode resultar em banimento do repo, e ou medidas legais para os usuários executores das ações inadequadas, que deverão asumir a responsabilidade legal/jurídica total.

Dados via Receita Federal (domínio público) e Brasil API.

## 🎯 Utilidade

Atualizar uma base de dados de clientes com CNPJ e Razão social, para verificar se o CNPJ esta ativo, atualizr o endereço, telefone, e-mail etc...

## ⚙️ Linguagens e ferramentas utilizadas

- Python
- Visual Studo Code
- Pandas
- Openpyxl
- Requestes
- datetime

## 🧩 Modo de construção

A lista CNPJ's e razão social foi extraida de um ERP, e o restante das informações ficaram em branco para serem consultadas.

A estrutura da planilha pode ser alterada, inserindo mais informações, porém você deve verificar a lista de dados da base da receita federal, se ela tem as informações que você precisa, para não ter erro. A partir disso, você altera o excel e o codigo.

## 📃 Instruções de uso

Consruir um excel com os CNPJ's e Razão social que vcê quer consultar, criar as colunas e ajustar o codigo para que a referência seja correspondente.

Considere que para cada consulta, o tempo estimado seja de 16 segundos, então se a base tem 50 linhas, multiplique por 16 para saber o tempo em segundos, depois divida por 60 para saber o tempo estimado em minutos, que será necessário para o programa realizar todas as consultas.

**Este projeto é para prospecção legítima, segmentação estratégica e objetivos acadêmicos, apenas.**

- ✅ **Permitido**: Análises de mercado, estudos de dados públicos CNPJ para MPEs.
- ❌ **Proibido**: Envio de spam, e-mails não solicitados, telemarketing abusivo, violações LGPD ou Políticas GitHub.

O uso indevido pode resultar em banimento do repositorio, e ou medidas legais para os usuários executores das ações inadequadas, que deverão asumir a responsabilidade legal/jurídica total.
