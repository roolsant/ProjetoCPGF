import os
import requests
import zipfile
from io import BytesIO

# Função para baixar e extrair arquivos
def download_and_extract(year, month, save_dir):
    month_str = str(month).zfill(2)  # Adiciona zero à esquerda para meses com um dígito
    url = f"https://portaldatransparencia.gov.br/download-de-dados/cpgf/{year}{month_str}"
    response = requests.get(url)
    
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as thezip:
            for zipinfo in thezip.infolist():
                if zipinfo.filename.endswith('.csv'):
                    zipinfo.filename = f"{year}_{month_str}_{zipinfo.filename}"
                    thezip.extract(zipinfo, save_dir)
        print(f"Arquivo {year}_{month_str} baixado e extraído com sucesso.")
    else:
        print(f"Falha ao baixar o arquivo para {year}_{month_str}. Código de status: {response.status_code}")

# Diretório para salvar os arquivos CSV
save_dir = './cpgf_csv'
os.makedirs(save_dir, exist_ok=True)

# Anos e meses disponíveis
anos = list(range(2013, 2025))
meses = list(range(1, 13))  # Meses de 1 a 12

# Baixar arquivos de 2013 a 2023 (todos os meses)
for ano in range(2013, 2024):
    for mes in meses:
        download_and_extract(ano, mes, save_dir)

# Baixar arquivos de 2024 (apenas até Maio)
for mes in meses[:5]:
    download_and_extract(2024, mes, save_dir)
