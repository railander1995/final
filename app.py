
import streamlit as st
import requests
import base64
import tempfile
import os

st.set_page_config(page_title="🔍 Consulta CNPJ e SINTEGRA AP", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #f0f8ff;
            color: #003366;
        }
        .stButton>button {
            background-color: #0056b3;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            padding: 10px;
        }
        .stTextInput>div>input {
            background-color: #ffffff;
            border: 1px solid #cce;
            border-radius: 6px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📱 Consulta CNPJ & SINTEGRA AP")
st.caption("Aplicativo inspirado em visual mobile com integração via API Infosimples")

cnpj = st.text_input("Digite o CNPJ (somente números)", max_chars=14)

# Token fixo
token = "J5VHHc9RJgeyTBzeARK43R5A5a8PWXiFDF5OmulT"

base_url = "https://api.infosimples.com/api/v2/consultas"

def extrair_link_pdf(dados_json):
    if isinstance(dados_json, str) and dados_json.endswith(".pdf") and dados_json.startswith("http"):
        return dados_json
    if isinstance(dados_json, dict):
        for key, val in dados_json.items():
            link = extrair_link_pdf(val)
            if link:
                return link
    if isinstance(dados_json, list):
        for item in dados_json:
            link = extrair_link_pdf(item)
            if link:
                return link
    return None

def baixar_pdf(link, nome_arquivo):
    r_pdf = requests.get(link)
    if r_pdf.status_code == 200:
        path = os.path.join(tempfile.gettempdir(), nome_arquivo)
        with open(path, "wb") as f:
            f.write(r_pdf.content)
        return path
    return None

if st.button("🔎 Consultar Agora"):
    if not cnpj:
        st.warning("Informe o CNPJ para continuar.")
    else:
        parametros = {
            "cnpj": cnpj,
            "token": token,
            "timeout": 600,
            "ignore_site_receipt": 0
        }

        st.subheader("📑 Comprovante de Inscrição no CNPJ")
        try:
            r = requests.get(f"{base_url}/receita-federal/cnpj", params=parametros)
            if r.status_code == 200:
                dados = r.json().get("data", [{}])[0]
                for k, v in dados.items():
                    st.write(f"**{k.replace('_', ' ').title()}**: {v}")
                link_pdf = extrair_link_pdf(dados)
                if not link_pdf:
                    link_pdf = extrair_link_pdf(r.json().get("site_receipts", []))
                if link_pdf:
                    path = baixar_pdf(link_pdf, "comprovante_cnpj.pdf")
                    if path:
                        with open(path, "rb") as f:
                            st.download_button("📥 Baixar PDF do CNPJ", f, file_name="comprovante_cnpj.pdf")
                else:
                    st.warning("⚠️ Nenhum PDF encontrado.")
            else:
                st.error(f"Erro na requisição: {r.status_code}")
        except Exception as e:
            st.error(f"Erro: {e}")

        st.subheader("🧾 Consulta SINTEGRA Amapá")
        try:
            r2 = requests.get(f"{base_url}/sintegra/ap", params=parametros)
            if r2.status_code == 200:
                dados2 = r2.json().get("data", [{}])[0]
                for k, v in dados2.items():
                    st.write(f"**{k.replace('_', ' ').title()}**: {v}")
                link_pdf2 = extrair_link_pdf(dados2)
                if not link_pdf2:
                    link_pdf2 = extrair_link_pdf(r2.json().get("site_receipts", []))
                if link_pdf2:
                    path2 = baixar_pdf(link_pdf2, "sintegra_ap.pdf")
                    if path2:
                        with open(path2, "rb") as f:
                            st.download_button("📥 Baixar PDF SINTEGRA AP", f, file_name="sintegra_ap.pdf")
                else:
                    st.warning("⚠️ Nenhum PDF encontrado.")
            else:
                st.error(f"Erro na requisição: {r2.status_code}")
        except Exception as e:
            st.error(f"Erro: {e}")
