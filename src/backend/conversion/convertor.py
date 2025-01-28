import pdfkit
import os

from backend.gpt_utils.gpt_analysis_env import GptAnalysisEnv
from backend.conversion.mrk_to_html import generate_html
from backend.conversion.conversion_toolkit import FileConverterToolkit

class Convertor:
    def __init__(self, analysis_env: GptAnalysisEnv):
         self._analysis_env = analysis_env 
        
    def to_markdown(self, language: str) -> str:
        file_path = "temp/output.md"
        with open(file_path, "w+", errors="ignore") as fstream:
            fstream.write(self._analysis_env.summarize_conversation(language=language))
        return file_path
    
    def to_html(self, language: str) -> str:
        file_path = "temp/output.html"
        generate_html(
            analysis_env=self._analysis_env, 
            output_path=file_path,
            language=language
            )
        return file_path
        
    
    def to_pdf(self, language) -> str:
        """Produces a pdf file from the analysis and returns its path"""
        output_pdf_path = "temp/output.pdf"
        converter_toolkit = FileConverterToolkit()
        converter_toolkit.convert_markdown(
            markdown_text=self._analysis_env.summarize_conversation(language=language),
            output_file=output_pdf_path,
            output_format="PDF")
        return output_pdf_path
    
    def to_word(self, language) -> str:
        """Produces a word file from the analysis and returns its path"""
        output_pdf_path = "output.docx"
        pass
        return output_pdf_path