import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import local_tokenizer
import sentencepiece
import google.protobuf
import time
import warnings
from google.genai import local_tokenizer
warnings.filterwarnings("ignore")
load_dotenv()

# Link to Tutorial
# https://app.dataquest.io/c/169/m/909/guided-project%3A-developing-a-dynamic-ai-chatbot/1/developing-a-dynamic-ai-chatbot

# Use Gemini ai




class ConversationManager:
    def __init__(self, gemini_key=None, base_url=None):
        self.gemini_key = os.environ["GEMINI_API_KEY"]
        self.client = genai.Client(api_key=self.gemini_key)
            
        self.conversation_history = []
        self.model = "gemini-3.1-flash-lite"
    def chat_completion(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        content = [
            {"role": msg["role"], "parts": [{"text": msg["content"]}]}
            for msg in self.conversation_history
        ]
        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model = self.model,
                    contents = content,
                    config=types.GenerateContentConfig(
                        # temperature=0,
                        # top_p=0.95,
                        # top_k=20,
                        max_output_tokens=2000
                    )
                )
                ai_response = response.text
                self.conversation_history.append({"role": "model", "content": ai_response})
                
                tokenizer = local_tokenizer.LocalTokenizer(model_name="gemini-2.5-flash-lite")
                result = tokenizer.count_tokens(content)
                token_manager = int(result.total_tokens)
                # print(token_manager)
                while True:
                    if token_manager > 50000:
                        self.conversation_history.pop(1)
                        tokenizer = local_tokenizer.LocalTokenizer(model_name= "gemini-2.5-flash-lite")
                        content = [
                            {"role": msg["role"], "parts": [{"text": msg["content"]}]}
                            for msg in self.conversation_history
                        ]
                        result = tokenizer.count_tokens(content)
                        token_manager = int(result.total_tokens)
                    else:
                        break
                return ai_response
            except Exception as e:
                if attempt < 2:
                    print(f"Error: {e}")
                    time.sleep(2)
                else:
                    print("Server is unavailable. Please try again")
                    self.conversation_history.pop()
                    return None
                    
level = " "
chat_manager = ConversationManager()
while True:
    level = input("Please enter the number corresponding to your spanish level:\n\n\
1. Beginner 2. Intermediate 3. Advanced\n").lower()
    if level == "1" or level =="beginner":
        chat_manager.conversation_history.append({
            "role": "user",
            "content": "You are a Spanish Language tutor. You help Students to learn Spanish and are friendly, but also honest and direct in order to help your students learn. You prioritize having spanish conversations with them, defining unknown words, and adjusting according to the users ability. When they make a mistake, correct them. Give encouragement when needed. The person you are teaching is a beginner in spanish. Focus on giving translations in english initially to help them understand. Always give a translation with a new word"
        }) 
        break
    elif level == "2" or level == "intermediate":
        chat_manager.conversation_history.append({
            "role": "user",
            "content": "You are a Spanish Language tutor. You help Students to learn Spanish and are friendly, but also honest and direct in order to help your students learn. You prioritize having spanish conversations with them, defining unknown words, and adjusting according to the users ability. When they make a mistake, correct them. Give encouragement when needed. The person you are teaching knows Intermediate spanish. Focus on more common words in conversation, while also occasionally adding in more advanced ones to help them learn."
        }) 
        break
    elif level == "3" or level == "advanced":
        chat_manager.conversation_history.append({
            "role": "user",
            "content": "You are a Spanish Language tutor. You help Students to learn Spanish and are friendly, but also honest and direct in order to help your students learn. You prioritize having spanish conversations with them, defining unknown words, and adjusting according to the users ability. When they make a mistake, correct them. Give encouragement when needed. The person you are teaching knows Advanced spanish"
        })
        break
    else:
        print("An Invalid input was made. Please made a valid input.\n")
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