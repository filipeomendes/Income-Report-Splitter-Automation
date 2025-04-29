import pdfplumber
import re
import os
import string
from PyPDF2 import PdfReader, PdfWriter

def limpar_nome_arquivo(nome):
    """Remove caracteres inválidos para nomes de arquivo"""
    nome_limpo = nome.strip()
    nome_limpo = re.sub(r'\s+', '_', nome_limpo)
    caracteres_validos = "-_.() %s%s" % (string.ascii_letters, string.digits)
    nome_limpo = ''.join(c for c in nome_limpo if c in caracteres_validos)
    return nome_limpo[:100]  # Limitar tamanho do nome do arquivo

def formatar_cpf(cpf):
    """Remove pontos e traço do CPF"""
    return re.sub(r'\D', '', cpf)  # Remove tudo que não for número

def separar_informes_por_beneficiario(arquivo_entrada):
    diretorio_saida = "informes_separados"
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)

    paginas_por_beneficiario = {}
    beneficiario_atual = None
    cpf_atual = None  

    padrao_cpf = re.compile(r'CPF:\s*(\d{3}\.\d{3}\.\d{3}-\d{2})')
    padrao_beneficiario = re.compile(r'Beneficiário:\s*(.*?)(?=\n|$)')

    try:
        with pdfplumber.open(arquivo_entrada) as pdf:
            for i, pagina in enumerate(pdf.pages):
                try:
                    texto = pagina.extract_text()
                    match_cpf = padrao_cpf.search(texto)

                    if match_cpf:
                        cpf_atual = formatar_cpf(match_cpf.group(1))  # Formatar CPF para senha
                        match_beneficiario = padrao_beneficiario.search(texto)

                        if match_beneficiario:
                            beneficiario_atual = match_beneficiario.group(1)
                        else:
                            beneficiario_atual = f"Sem_Nome_CPF_{cpf_atual}"

                        if beneficiario_atual not in paginas_por_beneficiario:
                            paginas_por_beneficiario[beneficiario_atual] = {"paginas": [], "cpf": cpf_atual}

                    if beneficiario_atual:
                        paginas_por_beneficiario[beneficiario_atual]["paginas"].append(i)

                except Exception as e:
                    print(f"Erro ao processar página {i+1}: {str(e)}")

        pdf_reader = PdfReader(arquivo_entrada)

        for beneficiario, dados in paginas_por_beneficiario.items():
            try:
                nome_arquivo = limpar_nome_arquivo(beneficiario) + ".pdf"
                caminho_completo = os.path.join(diretorio_saida, nome_arquivo)

                pdf_writer = PdfWriter()
                for num_pagina in dados["paginas"]:
                    pdf_writer.add_page(pdf_reader.pages[num_pagina])

                # Adicionar senha ao PDF
                senha = dados["cpf"]
                pdf_writer.encrypt(senha)

                with open(caminho_completo, "wb") as arquivo_saida:
                    pdf_writer.write(arquivo_saida)

                print(f"Arquivo criado: {nome_arquivo} (Senha: {senha})")
            except Exception as e:
                print(f"Erro ao criar PDF para '{beneficiario}': {str(e)}")

    except Exception as e:
        print(f"Erro ao abrir o arquivo PDF: {str(e)}")

if __name__ == "__main__":
    arquivo_entrada = "Informes.pdf"
    separar_informes_por_beneficiario(arquivo_entrada)
