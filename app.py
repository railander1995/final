
import streamlit as st
import requests
from pathlib import Path

st.set_page_config(page_title="Consulta CNPJ & SINTEGRA AP", layout="centered")

st.title("📱 Consulta CNPJ & SINTEGRA AP")
st.caption("Aplicativo inspirado em visual mobile com integração via API Infosimples")

cnpj = st.text_input("Digite o CNPJ (somente números)", max_chars=14)

if cnpj:
    api_token = "J5VHHc9RJgeyTBzeARK43R5A5a8PWXiFDF5OmulT"
    headers = {"Content-Type": "application/json"}

    # Consulta Receita Federal (CNPJ)
    url_cnpj = f"https://api.infosimples.com/api/v2/consultas/receita-federal/cnpj?token={api_token}&timeout=600&ignore_site_receipt=0&cnpj={cnpj}"
    r_cnpj = requests.get(url_cnpj, headers=headers)
    data_cnpj = r_cnpj.json()

    if "site_receipts" in data_cnpj and data_cnpj["site_receipts"]:
        pdf_url = data_cnpj["site_receipts"][0]
        pdf_path = Path(f"./pdfs/comprovante_cnpj_{cnpj}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(requests.get(pdf_url).content)
        st.success("📄 Comprovante de Inscrição no CNPJ disponível:")
        st.download_button("📥 Baixar Comprovante CNPJ", data=open(pdf_path, "rb"), file_name=pdf_path.name)

    # Consulta SINTEGRA AP
    url_sintegra = f"https://api.infosimples.com/api/v2/consultas/sintegra/ap?token={api_token}&timeout=600&ignore_site_receipt=0&cnpj={cnpj}"
    r_sintegra = requests.get(url_sintegra, headers=headers)
    data_sintegra = r_sintegra.json()

    if "site_receipts" in data_sintegra and data_sintegra["site_receipts"]:
        pdf_url = data_sintegra["site_receipts"][0]
        pdf_path = Path(f"./pdfs/comprovante_sintegra_ap_{cnpj}.pdf")
        with open(pdf_path, "wb") as f:
            f.write(requests.get(pdf_url).content)
        st.success("📄 Comprovante SINTEGRA AP disponível:")
        st.download_button("📥 Baixar Comprovante SINTEGRA", data=open(pdf_path, "rb"), file_name=pdf_path.name)
