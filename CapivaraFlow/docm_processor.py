from docx import Document
from docx.enum.text import WD_COLOR_INDEX
import os

def seu_prompt_llm(texto_original):
    """
    Função simulada para interagir com um modelo LLM.
    Neste exemplo, apenas adiciona um prefixo ao texto.
    """
    print(f"LLM: Processando texto original: '{texto_original}'")
    return f"[EDITADO POR LLM] {texto_original}"

def processar_docm(caminho_arquivo):
    """
    Processa um arquivo DOCM (tratado como DOCX) para detectar e editar
    texto destacado em amarelo.
    """
    temp_docx_path = None
    try:
        # Criar uma cópia temporária com extensão .docx
        nome_base, _ = os.path.splitext(os.path.basename(caminho_arquivo))
        temp_docx_path = os.path.join(os.path.dirname(caminho_arquivo), f"{nome_base}_temp.docx")
        
        # Copiar o conteúdo do .docm para o .docx temporário
        with open(caminho_arquivo, 'rb') as src, open(temp_docx_path, 'wb') as dst:
            dst.write(src.read())

        doc = Document(temp_docx_path)
        modificado = False

        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                if run.font.highlight_color == WD_COLOR_INDEX.YELLOW:
                    texto_original = run.text
                    texto_editado = seu_prompt_llm(texto_original)
                    run.text = texto_editado
                    modificado = True
        
        if modificado:
            caminho_saida = os.path.join(os.path.dirname(caminho_arquivo), f"{nome_base}_editado.docx")
            doc.save(caminho_saida)
            print(f"Arquivo '{caminho_arquivo}' processado e salvo como '{caminho_saida}'")
        else:
            print(f"Nenhum texto destacado em amarelo encontrado em '{caminho_arquivo}'.")

    except Exception as e:
        print(f"Erro ao processar o arquivo '{caminho_arquivo}': {e}")
    finally:
        # Remover o arquivo .docx temporário, se existir
        if temp_docx_path and os.path.exists(temp_docx_path):
            os.remove(temp_docx_path)
            print(f"Arquivo temporário '{temp_docx_path}' removido.")

if __name__ == "__main__":
    pasta_relatorios = "relatoriosExemplo"
    
    if not os.path.exists(pasta_relatorios):
        print(f"A pasta '{pasta_relatorios}' não foi encontrada.")
    else:
        for nome_arquivo in os.listdir(pasta_relatorios):
            if nome_arquivo.endswith(".docx") and not nome_arquivo.endswith("_temp.docx"):
                caminho_completo = os.path.join(pasta_relatorios, nome_arquivo)
                print(f"\nIniciando processamento de: {caminho_completo}")
                processar_docm(caminho_completo)