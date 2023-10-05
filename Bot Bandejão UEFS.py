import requests
from lxml import html
import os
from time import sleep
import pandas as pd
import pdfplumber
import datetime 

# Define o diretorio do sistema para evitar erros.
caminho_absoluto = os.path.abspath(__file__)
diretorio = os.path.dirname(caminho_absoluto)
caminho = f'{diretorio}\\arquivo'

def baixar_arquivo():
    if os.path.exists(caminho):
        os.remove(caminho)
        sleep(2)
    # URL da página web que contém o link para o arquivo Python
    url_da_pagina = 'http://www.propaae.uefs.br/modules/conteudo/conteudo.php?conteudo=15'

    # XPath para o link do arquivo Python dentro da página web
    xpath_do_link = '//*[@id="page"]/div[12]/a[2]'

    # Fazer o download da página web
    response = requests.get(url_da_pagina)

    if response.status_code == 200:
        # Analisar o conteúdo HTML da página
        tree = html.fromstring(response.content)

        # Encontrar o link para o arquivo Python usando XPath
        link_do_arquivo = tree.xpath(xpath_do_link)

        if link_do_arquivo:
            # Obter o URL completo do arquivo Python
            url_do_arquivo = link_do_arquivo[0].get('href')

            # Fazer o download do arquivo Python
            response_arquivo = requests.get(url_do_arquivo)

            if response_arquivo.status_code == 200:
                # Salvar o conteúdo do arquivo em um arquivo local
                with open(caminho, 'wb') as arquivo_local:
                    arquivo_local.write(response_arquivo.content)
                    print('Arquivo baixado')

if not os.path.exists(caminho):
    baixar_arquivo()
    sleep(5)

# Tenta abrir o arquivo(caso seja excel), se não, converte o pdf para excel.
try: 
    arquivo_excel = pd.read_excel(caminho)
    excel = arquivo_excel
except:
    pdf_path = caminho

    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            data.extend(table)

    df = pd.DataFrame(data)

    excel_path = f'{diretorio}\\excel.xlsx'
    if not os.path.exists(excel_path):
        os.rename(caminho, excel_path)

    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        worksheet = writer.sheets['Sheet1']

        for column in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            worksheet.column_dimensions[column[0].column_letter].width = max_length
    excel = excel_path

opcoes = [1, 2, 3 , 4]
comando = 0 

while not comando in opcoes: 
    while True:
        comando = input("Digite o comando correspondente:\n1- Cardápio de agora\n2- Cardápio de Hoje\n3- Atualizar Cardápio\n4- Sobre o Bot\n")
        try:
            comando = int(comando)
            break
        except ValueError:
            print("A entrada não é um número válido.")
            sleep(1)
    
    day_number = datetime.date.today().weekday()
    excel = pd.read_excel(f'{diretorio}\\excel.xlsx')
    df = pd.DataFrame(excel)
    df = df.set_index(1)
    dia = df[day_number + 2].str.replace('\n', ' ')
    data = df[day_number + 2]

    if comando == 1:
        if datetime.datetime.now().time() < datetime.time(9,0,0):
            print(f' CAFÉ DA MANHÃ - {data.iloc[1]} '.center(38, '~'))
            print(dia[4:9].to_string(name=False))

        elif datetime.datetime.now().time() > datetime.time(9,0,0) and datetime.datetime.now().time() < datetime.time(14,30,0):
            print(f' ALMOÇO - {data.iloc[1]} '.center(69, '~'))
            print(dia[11:21].to_string(name=False))

        else:
            print(f' JANTAR - {data.iloc[1]} '.center(63, '~'))
            print(dia[23:31].to_string(name=False))

    elif comando == 2:
        print(f' Cardapio de Hoje - {data.iloc[1]} '.center(38, '~'))
        print('')
        print(f' CAFÉ DA MANHÃ - {data.iloc[1]} '.center(38, '~'))
        print(dia[4:9].to_string(name=False))
        print('')
        print(f' ALMOÇO - {data.iloc[1]} '.center(70, '~'))
        print(dia[11:21].to_string(name=False))
        print('')
        print(f' JANTAR - {data.iloc[1]} '.center(63, '~'))
        print(dia[23:31].to_string(name=False))


    elif comando == 3:
        baixar_arquivo()
    
    elif comando == 4:
        print("""\nBot criado com fins de uso pela comunidade da UEFS e servir como meio didático.
O Bot atualiza o arquivo do cardápio de acordo com o site oficial do restaurante univesitário!
Contato com o dev: andersonx775@hotmail.com
Pagina do GitHub do bot: https://github.com/AndersoonReis/Bot-RU-UEFS
""")

    else:
        print('Comando inválido, tente novamente:')
        sleep(1)