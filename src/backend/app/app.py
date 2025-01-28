from enum import Enum

from backend.gpt_utils.gpt_client import GptClient
from backend.gpt_utils.gpt_analysis_env import GptAnalysisEnv

class App:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create and store it.
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        #if not hasattr(self, "_is_connected"):
        #    self._is_connected = False
        pass
     
    