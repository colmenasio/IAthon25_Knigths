import markdown
from backend.gpt_utils.gpt_analysis_env import GptAnalysisEnv

def generatehtml(analysis_env: GptAnalysisEnv):
    # Contenido en formato Markdown
    markdown_text = analysis_env.summarize_conversation()

    # Convertir de Markdown a HTML
    html_output = markdown.markdown(markdown_text)

    # Guardar el HTML resultante en un archivo
    with open(" ", "w", encoding="utf-8") as file:
        file.write(html_output)
