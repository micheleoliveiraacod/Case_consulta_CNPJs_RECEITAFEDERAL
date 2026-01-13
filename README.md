# ⚙️ Automação de tarefas administrativas

## 📢 Sobre
Este codigo atualiza o cadastro de um dataset de clientes de uma empresa. Ele consulta por API, no site da Receita Federal e do BrasilAPI os dados das colunas em brando no excel , com base no numero do CNPJ informado.

OBS: A execução deste tipo de automação compromete a usuabilidade do computador. Então ele é recomendado para projetos de automação com baixa frequência no fluxo de trabalho.
Ou que você tenha um computador exclusivo para rodar este programa e não comprometa as atividades de trabalho rotineiras.

## 🎯 Utilidade

Atualizar uma base de dados de clientes, verificar se o CNPJ esta ativo, atualizr o endereço, telefone, e-mail e socios.

## ⚙️ Linguagens e ferramentas utilizadas

RPA com Python e Visual Studo Code.

Pacotes pandas, pyautogui, openpyxl requestes e datetime.

## 🧩 Modo de construção

O codigo foi escrito e testado no vscode.

A lista CNPJ's e razão social fio extraida de um ERP, e o restante ds informações ficaram em branco para serem consultadas.

Esta parte de estrutura da planilha pode ser alterada, inserindo mais informações, porém você deve verificar a lista de dados que é possivel extrair destes sites antes, para não ter erro.

## 📃 Instruções de uso

Consruir um excel com os CNPJ's que vcê quer consultar, criar as colunas e ajustar o codigo para que o nome seja correspondente.

Considere que para cada consulta, o tempo estimado seja de 16 segundos, então se a base tem 50 linhas, multiplique por 16 para saber o tempo em segundos, depois divida por 60 para saber o tempo estimado em minutos que será necessário para o programa realizar todas as consultas.

## 🌐 Colaborações

Aberto.
