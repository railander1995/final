
import streamlit as st
import requests
import tempfile
import os

st.set_page_config(page_title="📄 Emissão de Certidões CNPJ + SINTEGRA", layout="centered")

st.title("📎 Gerador de Certidões")
st.caption("Emitir diretamente os arquivos PDF — sem exibir os dados.")

cnpj = st.text_input("Digite o CNPJ da empresa:", max_chars=18, value="15347020000100")

# Token fixo
token = "J5VHHc9RJgeyTBzeARK43R5A5a8PWXiFDF5OmulT"
base_url = "https://api.infosimples.com/api/v2/consultas"

def extrair_link_pdf(dados_json):
    if isinstance(dados_json, str) and dados_json.endswith(".pdf") and dados_json.startswith("http"):
        return dados_json
    if isinstance(dados_json, dict):
        # Caso especial: campo único 'site_receipt'
        if "site_receipt" in dados_json and isinstance(dados_json["site_receipt"], str):
            if dados_json["site_receipt"].endswith(".pdf"):
                return dados_json["site_receipt"]
        for val in dados_json.values():
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

if st.button("📤 Emitir Certidões"):
    if not cnpj:
        st.warning("⚠️ Digite um CNPJ válido.")
    else:
        parametros = {
            "cnpj": cnpj,
            "token": token,
            "timeout": 600,
            "ignore_site_receipt": 0
        }

        # CNPJ
        st.subheader("📑 Comprovante CNPJ")
        try:
            r = requests.get(f"{base_url}/receita-federal/cnpj", params=parametros)
            if r.status_code == 200:
                dados = r.json()
                link = extrair_link_pdf(dados)
                if link:
                    path = baixar_pdf(link, "comprovante_cnpj.pdf")
                    if path:
                        with open(path, "rb") as f:
                            st.download_button("⬇️ Baixar PDF CNPJ", f, file_name="comprovante_cnpj.pdf")
                else:
                    st.info("❌ PDF não encontrado para CNPJ.")
        except Exception as e:
            st.error(f"Erro: {e}")

        # SINTEGRA AP
        st.subheader("🧾 SINTEGRA Amapá")
        try:
            r2 = requests.get(f"{base_url}/sintegra/ap", params=parametros)
            if r2.status_code == 200:
                dados2 = r2.json()
                link2 = extrair_link_pdf(dados2)
                if link2:
                    path2 = baixar_pdf(link2, "sintegra_ap.pdf")
                    if path2:
                        with open(path2, "rb") as f:
                            st.download_button("⬇️ Baixar PDF SINTEGRA", f, file_name="sintegra_ap.pdf")
                else:
                    st.info("❌ PDF não encontrado para SINTEGRA.")
        except Exception as e:
            st.error(f"Erro: {e}")
