# Spanish AI Tutor
A CLI-based Spanish tutor powered by the Google Gemini API. This project acts as a conversational partner, helping you practice, maintain, or improve your Spanish fluency by providing real-time corrections and definitions.

## 🚀 How to Use
Once you have the project set up, running it is simple:
1. **Start the program:**
   ```bash
   python main.py
   ```
2. **Choose new or saved:** You'll be asked whether to start a **new** conversation or continue a **saved** one. If you choose new, you'll be asked whether to save this session (and if so, what to name it) before you begin.
3. **Select your level:** You will be prompted to enter a number (1, 2, or 3) or a keyword to set the difficulty:
   * **1 (Beginner):** Focuses on basic conversation with English translations.
   * **2 (Intermediate):** Conversational focus with a mix of common and advanced vocabulary.
   * **3 (Advanced):** Immersive, advanced-level conversation.
4. **Chat:** Simply type your message in Spanish. The tutor will respond, correct your mistakes, and define any new words.
5. **Exit:** Type `quit` at any time to end the session. If you chose to save, your conversation is written to disk automatically as you go.

## ✨ Key Features
* **Adaptive Persona:** The AI adjusts its vocabulary and teaching style based on your proficiency level (Beginner, Intermediate, or Advanced).
* **Real-time Tutoring:** The tutor acts as an active conversation partner, correcting grammatical errors and providing definitions for unknown words.
* **Persistent Sessions:** Conversations can be named, saved to disk, and resumed later — the full history and difficulty level are restored exactly as you left them.
* **Token-Aware Memory:** The application automatically manages conversation history, trimming older interactions to stay within the API's memory limits while keeping the context relevant.
* **Resilient API Calls:** Automatically retries failed requests (up to 3 attempts) before failing gracefully, so a brief network hiccup doesn't lose your conversation.
* **Interactive Feedback:** Encouraging responses designed to help you stay motivated and confident in your language journey.

## The Story Behind the Project
I learned Spanish through two years of full-time immersion. Through that experience, I found that real conversation — not just memorization — is what actually builds fluency. I designed this tool to simulate that: a conversational partner you can practice with anytime, that corrects you and teaches new words the way a real exchange would.

## My Development Journey
I started this project about halfway through my first programming class, using a Dataquest tutorial to get a basic chatbot talking to an AI API. The tutorial was written for a different AI API than the one I wanted to use, so even early on I had to adapt its structure to the Google GenAI SDK — with a lot of help from Claude AI, since I was still learning the fundamentals and leaned on it heavily for both structure and debugging.

Over time, that's changed a lot. Features like the conversation-saving and naming system and the token-limiting logic reflect decisions I made more independently, with AI helping me learn and debug rather than shaping the design. In the later stages, its role shrank to mostly debugging and cleanup suggestions — not designing features.

### Technical Challenges
* **API Structure:** Learning to map my logic to the specific requirements of the Google GenAI SDK was a steep learning curve.
* **The Tokenizer Headache:** A major hurdle was managing conversation history. Because Google hasn't updated its local tokenizer library to fully support the newer Gemini models, I had to adapt and use the older model's tokenizer to estimate my token usage. This taught me a lot about working around library limitations in real-world development.
* **Reliability:** API calls can fail for all kinds of reasons — network issues, server-side errors, timeouts. I added retry logic so a single failed request doesn't kill the whole conversation, which taught me a lot about handling failure gracefully instead of assuming the happy path.

## Setup
1. Clone this repo:
   ```bash
   git clone https://github.com/cordellwinward/spanish-ai-tutor.git
   ```
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
   > This installs the exact, verified set of dependencies (including `google-genai`, `protobuf`, `sentencepiece`, and `python-dotenv`) needed to run this project, confirmed by testing in a clean environment.
3. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) — click **Create API key**, choose to create it in a new project (simplest option if you don't already have a Google Cloud project), and copy the key once it's generated.
4. Create a `.env` file in the folder and add your key:
   ```text
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Roadmap & Improvements
I am actively improving this to make it a better daily practice tool:
* **[ ] Automated Tests:** Adding unit tests around the token-limiting and save/load logic.
* **[ ] More Robust Error Handling:** Distinguishing between different failure types (network timeout vs. malformed response vs. rate limit) instead of catching all exceptions the same way, and adding handling throughout the project for rarer edge cases (corrupted save files, unexpected API responses, etc.).
* **[ ] Code Cleanup:** Refactoring the logic as I continue to learn more about Python and SDK best practices.
* **[ ] Known Issue — Conversation Name Sanitization:** Conversation names containing characters like `/` or `\` currently break the save path (e.g. a name with a slash is misread as a folder path). Needs input sanitization before a name is used to build a file path.

---
*Since this is my first project, I'm learning as I go. If you see ways to improve the code or have advice on better API practices, feel free to open an issue or send a PR!*