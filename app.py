
import os
import requests

# Exemplo de uso:
pdf_url = 'https://exemplo.com/arquivo.pdf'
pdf_path = os.path.join('certidoes', 'arquivo.pdf')

# Garantir que o diretório existe
os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

# Baixar e salvar o PDF
response = requests.get(pdf_url)
with open(pdf_path, 'wb') as f:
    f.write(response.content)
