import markdown
from backend.gpt_utils.gpt_analysis_env import GptAnalysisEnv

def generate_html(analysis_env: GptAnalysisEnv, output_path: str) -> None:
    # Contenido en formato Markdown
    markdown_text = analysis_env.summarize_conversation()

    # Convertir de Markdown a HTML
    html_output = markdown.markdown(markdown_text)

    # Guardar el HTML resultante en un archivo
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_output)
