import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import local_tokenizer
import time
import warnings
import json
warnings.filterwarnings("ignore")
load_dotenv()
CONVERSATION_NAMES_FILE = "conversation_names.json"

# Link to Tutorial
# https://app.dataquest.io/c/169/m/909/guided-project%3A-developing-a-dynamic-ai-chatbot/1/developing-a-dynamic-ai-chatbot


class ConversationManager:
    def __init__(self):
        self.gemini_key = os.environ["GEMINI_API_KEY"]
        self.client = genai.Client(api_key=self.gemini_key)
        self.conversation_history = []
        self.model = "gemini-3.1-flash-lite"
        self.tokenizer = local_tokenizer.LocalTokenizer(model_name="gemini-2.5-flash-lite")
        self.system_prompt = None
        self.is_saved = False
        self.conversation_name = None
        self.conversation_name_added_to_conversation_names_file = False
    
    def limit_token_usage(self, content):
        result = self.tokenizer.count_tokens(content)
        token_manager = int(result.total_tokens)
        # print(token_manager)
        while token_manager > 50000 and len(self.conversation_history) > 1:
            self.conversation_history.pop(0)
            content = [
                {"role": msg["role"], "parts": [{"text": msg["content"]}]}
                for msg in self.conversation_history
            ]
            result = self.tokenizer.count_tokens(content)
            token_manager = int(result.total_tokens)
        return content

    def chat_completion(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        content = [
            {"role": msg["role"], "parts": [{"text": msg["content"]}]}
            for msg in self.conversation_history
        ]
        content = self.limit_token_usage(content)
        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model = self.model,
                    contents = content,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_prompt,
                        max_output_tokens=2000
                        # temperature=0,
                        # top_p=0.95,
                        # top_k=20,
                    )
                )
                ai_response = response.text
                self.conversation_history.append({"role": "model", "content": ai_response})
                if self.is_saved:
                    self.save_conversation_history()
                return ai_response
            except Exception as e:
                if attempt < 2:
                    print(f"Error: {e}")
                    time.sleep(2)
                else:
                    print("Server is unavailable. Please try again")
                    self.conversation_history.pop()
                    return None
    def load_saved_conversation(self, conversation_name):
        with open(f"conversations/{conversation_name}.json") as file:
            saved_conversation = json.load(file)
        self.system_prompt = saved_conversation["system_prompt"]
        self.conversation_history = saved_conversation["conversation_history"]
        self.conversation_name = conversation_name
        self.conversation_name_added_to_conversation_names_file = True
        self.is_saved = True
    def save_conversation_history(self):
        json_object = {
            "system_prompt" : self.system_prompt,
            "conversation_history" : self.conversation_history
        }
        os.makedirs("conversations", exist_ok=True)
        with open(f"conversations/{self.conversation_name}.json", "w") as file:
            json.dump(json_object, file, indent = 2)
        if self.conversation_name_added_to_conversation_names_file == False:
            is_not_in_file = ensure_conversation_name_is_unique(self.conversation_name)
            if is_not_in_file:
                if os.path.exists(f"conversations/{CONVERSATION_NAMES_FILE}"):
                    with open(f"conversations/{CONVERSATION_NAMES_FILE}") as file:
                        names = json.load(file)
                else:
                    names = []
                names.append(self.conversation_name)
                with open(f"conversations/{CONVERSATION_NAMES_FILE}", "w") as file:
                    json.dump(names, file, indent=2)
                        
            self.conversation_name_added_to_conversation_names_file = True
def create_new_conversation():
    saved_coversation_name = None
    while True:
        saved_conversation = input("Let me ask you a few questions to set up this conversation:\n\n\
Would you like to save this conversation? (Y/N) ").lower()
        if saved_conversation in ("y", "yes"):
            while True:
                saved_coversation_name = input("What would you like to name this conversation? ").strip()
                is_unique_conversation_name = ensure_conversation_name_is_unique(saved_coversation_name)
                if is_unique_conversation_name:
                    break
                else:
                    print("You already have a conversation with this name. Please enter a unique conversation name.")
            is_saved = True
            break
        elif saved_conversation in ("n", "no"):
            print("This conversation will not be saved\n")
            is_saved = False
            break
        else:
            print("Invalid input. Please enter Y or N.\n")
    while True:
        level = input("Please enter the number corresponding to your spanish level:\n\n\
1. Beginner 2. Intermediate 3. Advanced\n").lower()
        if level == "1" or level =="beginner":
            system_prompt = "You are a Spanish Language tutor. You help Students to learn Spanish and are friendly, but also honest and direct in order to help your students learn. You prioritize having spanish conversations with them, defining unknown words, and adjusting according to the users ability. When they make a mistake, correct them. Give encouragement when needed. The person you are teaching is a beginner in spanish. Focus on giving translations in english initially to help them understand. Always give a translation with a new word"
            break
        elif level == "2" or level == "intermediate":
            system_prompt = "You are a Spanish Language tutor. You help Students to learn Spanish and are friendly, but also honest and direct in order to help your students learn. You prioritize having spanish conversations with them, defining unknown words, and adjusting according to the users ability. When they make a mistake, correct them. Give encouragement when needed. The person you are teaching knows Intermediate spanish. Focus on more common words in conversation, while also occasionally adding in more advanced ones to help them learn."
            break
        elif level == "3" or level == "advanced":
            system_prompt = "You are a Spanish Language tutor. You help Students to learn Spanish and are friendly, but also honest and direct in order to help your students learn. You prioritize having spanish conversations with them, defining unknown words, and adjusting according to the users ability. When they make a mistake, correct them. Give encouragement when needed. The person you are teaching knows Advanced spanish"
            break
        else:
            print("An Invalid input was made. Please made a valid input.\n")
    return system_prompt, is_saved, saved_coversation_name

def ensure_conversation_name_is_unique(conversation_name):
    if not os.path.exists(f"conversations/{CONVERSATION_NAMES_FILE}"):
        return True
    with open(f"conversations/{CONVERSATION_NAMES_FILE}") as file:
        names = json.load(file)
    return conversation_name not in names

def print_conversation_names():
    try:
        with open(f"conversations/{CONVERSATION_NAMES_FILE}") as file:
            names = json.load(file)
            for name in names:
                print(name)
    except FileNotFoundError as err:
        print("No past conversations found")

def main():
    chat_manager = ConversationManager()
    while True:
        conversation_type = input("Would you like to start a new conversation or continue a saved one? (Enter: 'NEW' or 'SAVED') ").lower().strip()
        if conversation_type == "new":     
            chat_manager.system_prompt, chat_manager.is_saved, chat_manager.conversation_name = create_new_conversation()
            break
        elif conversation_type == "saved":
            print_conversation_names()
            while True:
                try:
                    saved_conversation_name = input("Which conversation would you like to continue? ").strip()
                    chat_manager.load_saved_conversation(saved_conversation_name)
                    break
                except FileNotFoundError as err:
                    print("Conversation does not exsist. Please enter a valid conversation name.")
            break
        else:
            print("Invalid input. Please enter a valid response.\n")
    print("=" * 40)
    print("Welcome to your AI Spanish Tutor!\n\
        Type 'quit' to exit")
    print("-" * 40)
    while True:
        entry= input("Your prompt: ")
        if entry == "quit":
            break
        response = chat_manager.chat_completion(entry)
        print("-" * 40)
        print(f"AI Spanish Tutor: {response}")
        print("-" * 40)

if __name__ == "__main__":
    main()