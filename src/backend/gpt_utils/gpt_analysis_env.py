import pandas as pd
import numpy as np
import scipy
from scipy import stats
import io
import contextlib
from threading import Event

from backend.gpt_utils.gpt_client import GptClient
from backend.gpt_utils.conversation import Conversation


class GptAnalysisEnv:

    _gpt_client = GptClient()

    def __init__(self, user_prompt):
        ### DUMMY PROMPT
        self._user_prompt = user_prompt
        self._conversation =  Conversation(
        f"""
        You are a data analysis tool. There is a dataset stored as a panda dataframe you will have to extract relevant information from.
        For this task, a small virtual environment running Python 1.13 has been prepared for you. This environment will contain the panda dataframe in a variable named "df" as well as the following pre-imported libraries: 
        pandas as pd; numpy as np; scipy as scipy; scipy.stats as stats. DO NOT try to import other libraries. Use the pre-imported ones\n
        Finally, your environment contains `finish()` function to signal when you're done with your analysis.
        Every response you produce must be exclusively python code, as it will be executed in the virtual environment we have prepared for you. The standard output of said operation will be shown to you.
        In case en exception occurs, you will be notified, and it will be handled automatically. Afterwards you will be able to continue your analysis.\n
        Remember, every response you produce will be executed directly as python code, so refrain from using unnecessary formatting that might cause a SyntaxError.\n
        Your job is only to extract as much relevant information from this dataframe. Feel free to perform additional tests you consider interesting.\n
        Be as extensive as you must. A very in-depth analysis is preferred\n
        IT IS IMPERATIVE THAT every result to every tests and relevant results must be displayed in the standard output of your environment using `print` or similar.\n
        Once you are done you can signal it by executing the `finish()` function whit no arguments.\n\n

        Finally, we will provide a small summary of the contents of the dataframe to assist in your analysis as well as some guidelines.\n
        {
            user_prompt
        }
        \n
        You can start your analysis now.
        """
        )
        self._dataset = None
        self._finish_event = Event()
        self._env_context = {"__builtins__": __builtins__, "pd": pd, "np": np, "scipy": scipy,"stats": stats}

    def is_analyzed(self):
        return self._finish_event.is_set()
    
    def load_dataset(self, path):
        # Define a custom converter function
        def custom_converter(val):
            try:
            # Attempt to convert to a float or int
                if '.' in val:
                    return float(val)
                else:
                    return int(val)
            except ValueError:
            # Return the value as a string if conversion fails
                return str(val) 
        self._dataset = pd.read_csv(path, converters={col: custom_converter for col in pd.read_csv(path, nrows=0).columns})
        self._env_context["df"] = self._dataset

    
    def _parse_executable(self, message: str):
        if "```python" in message:
            message = message.split("```python")[1].split("```", 1)[0]
        else:
            message = message
        message.replace("exit()", "# exit_request").replace("quit()", "# exit_request")
        return message


    def _is_quit_request(self, message: str) -> bool:
        return "exit()" in message.lower() or "quit()" in message.lower()
   
    
    def analyze_dataset(self, do_log: bool = False):
        self._finish_event = Event()
        if self._dataset is None:
            raise ValueError("Dataset no loaded!")
        
        df = self._dataset.copy(deep=True)
        # Start the conversation
        assistant_response = self._gpt_client.continue_conversation(conversation=self._conversation, new_message=None)
        if do_log: print(f"[Response]\n {assistant_response}\n\n")
         
        # Main analysis loop
        def finish():
            print("Exiting Environment")
            self._finish_event.set()
             
        while True:
            # Run the code and capture the updated state or output
            executable_code = self._parse_executable(assistant_response)
            local_context= {"finish": finish}
            command_output = self._execute_and_capture(executable_code, local_context) 
            if do_log: print(f"[Std Output]\n {command_output}\n\n")
            if self._finish_event.is_set(): break
    
            # Continue the conversation with the user's message
            assistant_response = self._gpt_client.continue_conversation(
                conversation=self._conversation, 
                new_message=command_output
                )
            if do_log: print(f"[Response]\n {assistant_response}\n\n")


    def _execute_and_capture(self, code: str, extra_context: dict) -> str:
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            # Prepare the execution context (globals and locals)
            exec_globals = self._env_context # Ensure builtins and such are available
            if extra_context:
                exec_globals.update(extra_context)
            try: 
                exec(code, exec_globals)
            except Exception as e:
                return str(e)
        
        # Get the captured output as a string
        return captured_output.getvalue().strip()
    
    def dump_conversation(self):
        return self._conversation.dump_conversation()
    
    def summarize_conversation(self, language = "english"):
        system_prompt = f"""
        You are a data analyst\n
        Another data analyst was requested to analyze a dataset for you in python using libraries like pandas, scipy, etc...\n
        He, under the role of "system" executed a series of scripts in a python environment. The standard output of said scripts was stored under the role of "user"\n
        Your job is to study the analysis performed, understand what was done and produce a extensive and detailed report of the analysis.\n
        It is vital for your to ensure your report is formatted in markdown format.
        Finally, generate this markdown report in the following language: {language}.\n
        
        You will be provided the prompt the other analyst received as well as the full analysis performed.
        {{"previous_analyst_prompt": {self._user_prompt}, "full_analysis": {self.dump_conversation()}}} 
        """
        user_prompt = "Provide the report of the analysis"
        return self._gpt_client.produce_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt
            )
        
    def flush_conversation(self):
        self._conversation.flush_all_msgs() 