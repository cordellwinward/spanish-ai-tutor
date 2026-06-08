***

# Spanish AI Tutor

A CLI-based Spanish tutor powered by the Google Gemini API. This project acts as a conversational partner, helping you practice, maintain, or improve your Spanish fluency by providing real-time corrections and definitions.

## 🚀 How to Use
Once you have the project set up, running it is simple:

1. **Start the program:**
   ```bash
   python main.py
   ```
2. **Select your level:** You will be prompted to enter a number (1, 2, or 3) or a keyword to set the difficulty:
   * **1 (Beginner):** Focuses on basic conversation with English translations.
   * **2 (Intermediate):** Conversational focus with a mix of common and advanced vocabulary.
   * **3 (Advanced):** Immersive, advanced-level conversation.
3. **Chat:** Simply type your message in Spanish. The tutor will respond, correct your mistakes, and define any new words.
4. **Exit:** Type `quit` at any time to end the session.

## ✨ Key Features
*   **Adaptive Persona:** The AI adjusts its vocabulary and teaching style based on your proficiency level (Beginner, Intermediate, or Advanced).
*   **Real-time Tutoring:** The tutor acts as an active conversation partner, correcting grammatical errors and providing definitions for unknown words.
*   **Token-Aware Memory:** The application automatically manages conversation history, trimming older interactions to stay within the API's memory limits while keeping the context relevant.
*   **Interactive Feedback:** Encouraging responses designed to help you stay motivated and confident in your language journey.

## The Story Behind the Project
Over the last two years, I’ve been working hard to reach fluency in Spanish. I built this tool to act as my personal practice partner. It’s been an effective way to keep my conversational skills sharp without needing a human tutor.

## My Development Journey
This is my very first programming project. I’m new to coding, so this was a massive learning experience. I couldn't have completed this without the assistance of Claude AI to help me structure my logic and debug my code.

### Technical Challenges
*   **API Structure:** Learning to map my logic to the specific requirements of the Google GenAI SDK was a steep learning curve.
*   **The Tokenizer Headache:** A major hurdle was managing conversation history. Because Google hasn't updated its local tokenizer library to fully support the newer Gemini models, I had to adapt and use the older model's tokenizer to estimate my token usage. This taught me a lot about working around library limitations in real-world development.

## Setup
1. Clone this repo:
   ```bash
   git clone https://github.com/cordellwinward/spanish-ai-tutor.git
   ```
2. Install the required libraries:
   ```bash
   pip install google-generativeai python-dotenv
   ```
3. Create a `.env` file in the folder and add your key:
   ```text
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Roadmap & Improvements
I am actively improving this to make it a better daily practice tool:
*   **[ ] Persistent Sessions:** Implementing a way to save conversation history to a local file so I can pick up where I left off later.
*   **[ ] Proper System Instructions:** Refactoring the prompt handling to align with Google’s official standard for system instructions rather than using a manual chat injection.
*   **[ ] Code Cleanup:** Refactoring the logic as I continue to learn more about Python and SDK best practices.

---
*Since this is my first project, I’m learning as I go. If you see ways to improve the code or have advice on better API practices, feel free to open an issue or send a PR!*