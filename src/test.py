from backend.gpt_utils.conversation import Conversation
from backend.gpt_utils.gpt_client import GptClient

if __name__ == "__main__":
    convo = Conversation( system_msg=
        "You are Fiodor Dovstoyevski. Reply to the user messages like he would during a casual chat"
        )
    client = GptClient()
    while True:
        print(client.continue_conversation(conversation=convo, new_message=input("Your Message: ")))