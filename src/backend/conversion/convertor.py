from backend.gpt_utils.gpt_analysis_env import GptAnalysisEnv
from backend.conversion.mrk_to_html import generate_html

class Convertor:
    def __init__(self, analysis_env: GptAnalysisEnv):
         self._analysis_env = analysis_env
         
    def _to_html(self, language) -> str:
        """Produces a html file from the analysis and returns its path"""
        file_path = "temp/output.html"
        with open(file_path, "w+") as fstream:
            fstream.write(str(self._analysis_env.dump_conversation()))
        return file_path
        
    def to_html(self, language) -> str:
        file_path = "temp/output.html"
        generate_html(
            analysis_env=self._analysis_env, 
            output_path=file_path)
        return file_path
        
    
    def to_pdf(self, language) -> str:
        """Produces a pdf file from the analysis and returns its path"""
        pass
    
    def to_word(self, language) -> str:
        """Produces a word file from the analysis and returns its path"""
        pass