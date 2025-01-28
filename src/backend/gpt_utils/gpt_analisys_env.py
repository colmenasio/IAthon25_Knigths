import pandas as pd

from backend.gpt_utils.gpt_client import GptClient
from backend.gpt_utils.conversation import Conversation


class GptAnalisysEnv:

    _gpt_client = GptClient()

    def __init__(self):
        self._dataframe = None

        ### DUMMY PROMPT
        self._conversation =  Conversation(
        """
        You are a data analysis tool. There is a dataset stored as a panda dataframe you will have to extract relevant information from.
        For this task, a small virtual enviroment running Python 1.13 has been prepared for you. This enviroment will contain the dataframe in a variable named "dataframe" as well as most libraries you'll need.\n
        Every response you produce must be excusively python code, as it will be executed in the virtual enviroment we have prepared for you. The standart output of said operation will be shown to you.
        In case en exception occurs, you will be notified, and it will be handled automatically. Afterwards you will be able to continue your analysis.\n
        Remember, every response you produce will be executed directly as python code, so refrain from using unnecesary formatting that might cause a SyntaxError.\n
        Your job is only to extract as much relevant information from this dataframe.\n\n

        Finally, we will provide a small summary of the contents of the dataframe to assist in your analisys.\n
        Summary: 'data of a small food business about the tips given by customers'
        Collumns:{
        'age': 'age of the custome. int',
        'gender': 'gender of the customer, male being encoded as 0 and woman as 1. bool',
        'smoker': 'boolean representing wether the client smokes or not. bool'
        }
        Questions: 'can we statistically affirm that smokers give greaters tips?'\n\n

        You can start your analysis now.
        """
        )