
from backend.gpt_utils.gpt_client import GptClient
from backend.gpt_utils.gpt_analysis_env import GptAnalysisEnv
import argparse
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Running test")
    
    # Creación del parser de argumentos
    parser = argparse.ArgumentParser(description="Generador de informe en HTML de análisis de dataset.")
    parser.add_argument("--path_dataset", type=str, required=True, help="Análisis detallado del dataset.")
    # parser.add_argument("--dataset_analysis", type=str, required=True, help="Análisis detallado del dataset.")
    #parser.add_argument("--analysis_objectives", type=str, required=True, help="Objetivos del análisis.")
    #parser.add_argument("--file_path", type=str, required=True, help="Ruta donde se guardará el archivo HTML.")

    # Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    user_prompt = """
    Column Explanation:
    JAMB_Score: The score obtained by the student in the JAMB exam.
    Study_Hours_Per_Week: The number of hours the student spends studying each week.
    Attendance_Rate: The percentage of classes attended by the student.
    Teacher_Quality: A rating of the quality of teachers, on an unspecified scale.
    Distance_To_School: The distance (in kilometers) from the students home to their school.
    School_Type: The type of school the student attends (e.g., Public or Private).
    School_Location: The location of the school (e.g., Urban or Rural).
    Extra_Tutorials: Indicates whether the student participates in extra tutorials (Yes/No).
    Access_To_Learning_Materials: Whether the student has access to essential learning materials (Yes/No).
    Parent_Involvement: The level of involvement of the students parents in their education (e.g., Low, Medium, High).
    IT_Knowledge: The students level of IT knowledge (e.g., Low, Medium, High).
    Student_ID: A unique identifier for each student.
    Age: The age of the student in years.
    Gender: The gender of the student (e.g., Male, Female).
    Socioeconomic_Status: The socioeconomic status of the students household (e.g., Low, Medium, High).
    Parent_Education_Level: The highest education level achieved by the students parents (e.g., None, Primary, Secondary, Tertiary).
    Assignments_Completed: The number of assignments completed by the student.
    
    Guidelines:
    Test at least the statistic significance of Gender and School_Type on the JAMB_Score
    """
       
    analysis_env = GptAnalysisEnv(user_prompt=user_prompt)    
    analysis_env.load_dataset(args.path_dataset)
    analysis_env.analyze_dataset(do_log=True)

    # Obtenemos la salida de `dump_conversation()`
    conversation_history = analysis_env.dump_conversation()

    # Convertimos la conversación a un formato adecuado para texto
    conversation_history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    print(conversation_history_str)

    # Creación de la sesión del cliente GPT
    session = GptClient()

    # Prompt que describe la tarea a generar el HTML

    ### Instrucciones para completar el documento:
1. **Datos Dinámicos**: Reemplaza los placeholders en `<pre id="missing-values">`, `<pre id="t-test-results">`, y `<pre id="anova-results">` con los resultados correspondientes de tu análisis.
2. **Gráficos**: Asegúrate de guardar los gráficos generados en el análisis como `boxplot_gender.png` y `boxplot_school_type.png` en la misma carpeta donde se encuentra tu archivo HTML, o ajusta la ruta de las imágenes según sea necesario.
3. **Revisión**: Revisa y ajusta cualquier contenido según sea necesario para que refleje con precisión tu análisis y hallazgos.

Este doc

    prompt = (
    f"Queremos generar un documento HTML elegante y profesional para un análisis de consultoría, utilizando dos inputs principales:\n\n"
    f"1. Un dataset en formato dataframe.\n"
    f"2. Un análisis detallado del dataset en formato string {conversation_history_str}.\n\n"
    f"El documento debe incluir una descripción rigurosa del 'status quo' de los datos, antes de profundizar en el análisis. Esto implica evaluar el estado inicial de los datos de manera exhaustiva, incluyendo:\n\n"
    
    
    
    f"- Descripción general del dataset, destacando sus características, calidad de los datos, y posibles limitaciones.\n"
    f"- Identificación de valores nulos, inconsistencias o anomalías dentro del dataset, proporcionando una visión detallada del estado actual de los datos.\n"
    f"- Distribución de las variables, estadísticas descriptivas y cualquier tendencia evidente antes de proceder al análisis completo.\n\n"
    f"Una vez abordado el 'status quo' de los datos, el documento debe incluir el análisis realizado, organizado y estructurado de forma clara y comprensible. El análisis debe resaltar los principales hallazgos, evidenciar las correlaciones clave y proporcionar insights valiosos sobre el dataset.\n\n"
    f"Además, se deben incluir:\n\n"
    f"- Un índice que facilite la navegación del documento.\n"
    f"- Gráficos e imágenes relevantes generados a partir del dataset, acompañados de descripciones claras y análisis de cada uno.\n\n"
    f"En cuanto al diseño, queremos que apliques estilos CSS elegantes y profesionales, asegurando una estructura ordenada y visualmente atractiva. Los elementos clave a considerar son:\n\n"
    f"- Tipografía moderna y legible.\n"
    f"- Márgenes adecuados y espaciamiento suficiente entre las secciones.\n"
    f"- Títulos y subtítulos bien definidos para guiar al lector a través del documento de manera fluida.\n\n"
    f"El objetivo es crear un informe completo y profesional que no solo muestre el análisis, sino que también proporcione una visión detallada y rigurosa sobre el estado actual de los datos y las conclusiones derivadas."
    )

    # Solicitud de completar la tarea con el prompt definido
    result = session.produce_completion('Trabajas para una consultoria y eres experto de programacion en html. Tu tarea es crear un archivo de html basado en las siguientes especificaciones', prompt)

    with open("reporte.html", "w", encoding="utf-8") as file:
        file.write(result)

#& c:/Users/scarl/IAthon25_Knigths/.venv/Scripts/python.exe c:/Users/scarl/IAthon25_Knigths/src/str_to_html.py --path_dataset C:/Users/scarl/IAthon25_Knigths/src/data/Datasets/JAMB/jamb_exam_results.csv

    
