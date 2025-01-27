import requests
import json
import ast
from common.retiable import retriable

from backend.gpt_utils.conversation import Conversation

class OpenAIException(Exception):
    pass

def get_openai_key() -> str:
    try:
        with open("config/api_keys.json", "r") as fstream:
            return json.load(fstream)["openai_key"]
    except FileNotFoundError:
        raise FileNotFoundError("Missing api_keys.json in config folder")
    except KeyError:
        raise KeyError("Missing openai key in api_keys.json")
    

class GptClient:
    """Singleton managing api calls and sanitizing I-O"""

    _instance = None

    _key = get_openai_key()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create and store it.
            cls._instance = super().__new__(cls)
            cls._instance._is_connected = True
        return cls._instance
    
    def __init__(self):
        #if not hasattr(self, "_is_connected"):
        #    self._is_connected = False
        pass


    def _call_api(self, body, headers) -> requests.Response: 
        # Send the request to the API
        try:
            url = "https://api.openai.com/v1/chat/completions"
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()  # Raise an error for bad status codes
        except requests.RequestException as e:
            raise OpenAIException(f"API request failed: {e}")
        return response
     

    def _make_request(self, body, headers) -> str:
        try:
            response = self._call_api(body=body, headers=headers)
            return response.json()["choices"][0]["message"]["content"] 
        except KeyError:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            raise OpenAIException(f"API response error: {error_message}")
        except Exception as e:
            raise OpenAIException(f"Error ocurred when calling the openai api: {e}")

    def _generate_header(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._key}"
        }
    
    def _generate_body(self, msgs: list, temperature, max_tokens) -> dict:
        return {
            "model": "gpt-4o-mini",
            
            "messages": msgs,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

    def _produce_completion(self, 
                      system_prompt: str, 
                      user_prompt: str,
                      temperature=0.7, 
                      max_tokens=2000):
        """
        Function to call the ChatGPT API and retrieve a response.
        
        Parameters:
            prompt (str): The input text prompt for ChatGPT.
            api_key (str): Your API key for OpenAI.
            model (str): The model to use (default is "gpt-4o-mini").
            temperature (float): Sampling temperature to control randomness.
            max_tokens (int): Maximum number of tokens to generate.
        
        Returns:
            str: The content of the response from the API.
        """
        # Request payload
        body = self._generate_body(
            msgs=[{"role": "system", 
                   "content": system_prompt},
                   {"role": "user", 
                    "content": user_prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens)
        
        headers = self._generate_header()
        return self._make_request(body=body, headers=headers)

    
    @staticmethod
    def _parse_list(list_str: str) -> list[str]:
        try:
            parsed_list = ast.literal_eval(list_str)
        except ValueError as e:
            raise OpenAIException(f"ValueError caught: {e}")
        except SyntaxError as e:
            raise OpenAIException(f"SyntaxError caught: {e}")
        
        if not isinstance(parsed_list, list):
            raise OpenAIException("Chatgpt Response is not a list")
        if not all([isinstance(x, str) for x in parsed_list]):
            raise OpenAIException("Chatgpt Response is a list but its elements are not strings")
        
        return parsed_list 
        

    def _choose_option(self, user_prompt: str, possible_outputs: list, temperature=0.7, max_tokens=2000) -> str:
        system_prompt = f"""You are a tool whose job is to choose the best option from a list according to a certain criteria.\n
                            You will be given a prompt explaining the criteria to choose the value as well as list of possible options.\n
                            Your response should be exclusively the item you selected with the exact capitalization.\n
                            Your response must not include the quotations marks indicating a string"""
        formatted_user_prompt = f"""{{
        "criteria": {user_prompt}, 
        "options": {possible_outputs}
        }}"""
        result = self._produce_completion(system_prompt, formatted_user_prompt, temperature, max_tokens)
        if result not in possible_outputs:
            raise OpenAIException(f"The result '{result}' is not in the list of possible outputs.")
        return result


    def _produce_list(self, user_prompt: str, max_items = 10, temperature=0.7, max_tokens=2000) -> list[str]:
        system_prompt = f"""You are a tool whose job is to produce a list of strings according to a certain criteria. You will be passed this criteria and
                            you must generate a python list with the values you deem correct formatted always as strings.\n
                            This response should be exactly formatted as python list of strings, no more and no less.\n
                            This list should contain at most {max_items} items.\n
                            For example, if the criteria you received was "Produce a list of fruits" your output could be `["peach", "strawberry", "lemon"]`
                            """
        result = self._produce_completion(system_prompt, f'{{"criteria": "{user_prompt}"}}', temperature, max_tokens)
        return GptClient._parse_list(result)
    

    def _choose_subset(self, user_prompt: str, possible_outputs: list, temperature=0.7, max_tokens=2000) -> list[str]:
        system_prompt = f"""You are a tool whose job is to select a subset of options from a list of options according to a certain criteria.\n
                            You will be given a prompt explaining the criteria to follow when selecting the values as well as list of possible options to select.\n
                            Your response should be formatted as a python list with the item you selected with the exact capitalization as provided.\n
                            For example, if you received the options: `["apple", "banana", "lightbulb"]` and you decided to choose "apple" and "banana", your output should be just `["apple", "banana"]`"""
        formatted_user_prompt = f"""{{
        "criteria": {user_prompt}, 
        "options": {possible_outputs}
        }}"""
        result = self._produce_completion(system_prompt, formatted_user_prompt, temperature, max_tokens)
        choices = GptClient._parse_list(result)
        
        # Check if all the results are in the possible outputs set
        possible_outputs_set = set(possible_outputs) 
        if not set(choices).issubset(possible_outputs_set):
            raise OpenAIException(f"One or more responses are not valid. Expected only: {', '.join(possible_outputs)}")
        return choices

    @retriable(3, OpenAIException)
    def from_conversation(self, conversation: Conversation, new_message: str = None) -> str:
        """Use a previous conversation as a starting point for a request. Automatically Update the Conversation inner state
        Returns None if failed"""
        if new_message is not None:
            conversation.register_user_msg(new_message)

        headers = self._generate_header()
        body = self._generate_body(
            msgs=conversation.get_msgs_list(),
            temperature=0.7,
            max_tokens=3000
        )
        try:
            response = self._make_request(body=body, headers=headers)

            # Everything went rigth so we update the conversation
            conversation.register_assistant_msg(response)
            return response
        except OpenAIException:
            raise
        except Exception as e:
            if new_message is not None:
                conversation.rollback_msgs(1)
            return None 

    @retriable(3, OpenAIException)
    def produce_completion(self, system_prompt: str, user_prompt: str, temperature=0.7, max_tokens=2000) -> str:
        return self._produce_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens
            )

    @retriable(3, OpenAIException)
    def choose_option(self, user_prompt: str, possible_outputs: list, temperature=0.7, max_tokens=2000) -> str:
        return self.choose_option(user_prompt, possible_outputs, temperature, max_tokens)
    
    @retriable(3, OpenAIException)
    def produce_list(self, user_prompt: str, max_items = 10, temperature=0.7, max_tokens=2000) -> list[str]:
        return self._produce_list(user_prompt, max_items ,temperature, max_tokens)

    @retriable(3, OpenAIException)
    def choose_subset(self, user_prompt: str, possible_outputs: list, temperature=0.7, max_tokens=2000) -> list[str]:
        return self._choose_subset(user_prompt, possible_outputs, temperature, max_tokens)
