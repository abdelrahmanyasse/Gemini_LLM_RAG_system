# Jarvis Chatbot without Using LLM API

A simple rule-based chatbot built in Python.

## Features
- Input sanitization (unicode normalization, control char stripping)
- Keyword-based response matching
- Exit commands: `exit`, `quit`, `bye`, `goodbye`, `ciao`

## Requirements
Python 3.10+, no external dependencies.

## Run
python chatbot.py

--------------------------------------------------------------------------------------------------------------------

# Jarvis - AI Chatbot

A simple conversational chatbot powered by Google's Gemini API, with a friendly assistant persona named **Jarvis**.

---

## Features

- Conversational AI using `gemini-2.0-flash-lite`
- Persistent chat history within a session
- Input sanitization to clean and normalize user messages
- Simple exit commands to end the chat

---

## Requirements

- Python 3.7+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/abdelrahmanyasse/Simple_Chatbot
   cd Rule-based_Chatbot
   ```

2. **Install dependencies**

   ```bash
   pip install google-generativeai python-dotenv
   ```

3. **Set up your environment variables**

   Create a `.env` file in the root of the project:

   ```
   GEMINI_API_KEY=your_api_key_here
   ```

   > ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

---

## Usage

```bash
python jarvis.py
```

Then start chatting:

```
You: Hello, who are you?
Jarvis: I'm Jarvis, your helpful assistant! How can I help you today?
```

---

## Exiting the Chat

Type any of the following to end the session:

```
exit / quit / goodbye / bye / end chat / ciao
```

---

## How It Works

- Loads the Gemini API key from `.env` using `python-dotenv`
- Initializes a Gemini model with a custom system instruction (`"You are Jarvis, a helpful and friendly assistant."`)
- Starts a chat session with persistent history
- Sanitizes each user input by:
  - Stripping whitespace
  - Removing control characters
  - Collapsing extra spaces
  - Removing punctuation
  - Normalizing unicode (NFKC)
  - Converting to lowercase
- Sends the sanitized input to the model and prints the response

---

## Project Structure

```
.
├── Chatbot.py       # Main chatbot script
├── .env            # Your API key (not committed)
├── .gitignore      # Excludes .env and other sensitive files
└── README.md       # This file
```

---

## .env.example

```
GEMINI_API_KEY=your_api_key_here
```


