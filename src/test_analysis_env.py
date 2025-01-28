from backend.gpt_utils.gpt_analysis_env import GptAnalysisEnv

if __name__ == "__main__":
       
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
    analysis_env.load_dataset("data/jamb_exam_results.csv")
    analysis_env.analyze_dataset(do_log=True)
    print(analysis_env.summarize_conversation())
    print(analysis_env.dump_conversation())