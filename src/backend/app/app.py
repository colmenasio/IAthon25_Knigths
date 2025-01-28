from enum import Enum, auto

from backend.gpt_utils.gpt_client import GptClient
from backend.gpt_utils.gpt_analysis_env import GptAnalysisEnv
from backend.conversion.convertor import Convertor

class Format(Enum):
    PDF = auto()
    WORD = auto()
    HTML = auto()
    POWERPOINT = auto()

    def get_extension(self):
        match self:
            case Format.PDF:
                return ".pdf"
            case Format.WORD:
                return ".docx"
            case Format.HTML:
                return ".html"
            case Format.POWERPOINT:
                return ".pptx"

class App:
    
    _gpt_client = GptClient()
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create and store it.
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "_analysis_env"):
            self._analysis_env: GptAnalysisEnv = None
        if not hasattr(self, "_convertor"):
            self._convertor: Convertor = None
        if not hasattr(self, "_result_path"):
            self._result_path: str = None
    
    def perform_analysis(self, user_request: str, user_description: str, path_to_csv: str) -> None:
        """Performs a analysis over the given file"""
        self._analysis_env = GptAnalysisEnv(f"""{{
            "dataset_description": {user_description},
            "analysis_guidelines": {user_request}
        }}""") # Make a fresh environment
        self._analysis_env.load_dataset(path=path_to_csv)
        self._analysis_env.analyze_dataset(do_log=True)
    
    def produce_output(self, format: Format, language = "english") -> str:
        """Produces a result from an analysis and returns a path to the result"""  
        if not self._analysis_env.is_analyzed():
            raise ValueError("Can't produce output because no analysis has been performed")
        self._convertor = Convertor(self._analysis_env)
        match format:
            case Format.HTML:
                self._result_path = self._convertor.to_html(language)
            case Format.PDF:
                self._result_path = self._convertor.to_pdf(language)
            case Format.WORD:
                self._result_path = self._convertor.to_word(language) 
        return self._result_path

    def get_output_path(self) -> str:
        """Returns the result to the last analysis"""
        return self._result_path 