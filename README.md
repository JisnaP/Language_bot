# 🌍 LanguageBot - AI-Powered Language Learning Chatbot  

LanguageBot is an interactive chatbot that helps users practice and learn a new language through conversation. It detects and corrects mistakes, provides scenario-based dialogues, and tracks user progress.  

## 🚀 Features  
- 🌎 **Supports multiple languages** (French, Spanish, German, Arabic, etc.)  
- 🧑‍🏫 **Conversational AI** for real-time practice  
- ✅ **Grammar & spelling correction**  
- 📊 **Tracks mistakes and progress**  
- 🔍 **Scenario-based dialogues** (e.g., restaurant, airport, shopping)  
- 🖥️ **Web-based UI using Flask**  

## 🛠️ Installation  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/JisnaP/LanguageBot.git
   cd LanguageBot
   ```

2. **Create a virtual environment**  
   ```bash
   conda create -p ./env python=3.10 -y
   conda activate ./env
  ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Set up OpenAI API key and flask secret key**  
   Create a `.env` file and add:  
   ```ini
   OPENAI_API_KEY=your_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   ```

5. **Run the application**  
   ```bash
   python app.py
   ```

6. **Open in browser**  
   Visit `http://127.0.0.1:5000/` to start chatting.  

## 📜 Usage  
1. **Select your learning language, known language, and proficiency level.**  
2. **Engage in interactive conversations with the chatbot.**  
3. **Receive real-time grammar and spelling corrections.**  
4. **Get a summary of your mistakes at the end of the session.**  

## 📂 Project Structure  
```
LanguageBot/
│── lang_bot/               # Core chatbot logic  
│   ├── langbot.py      # Chatbot class and correction functions  
│── templates/              # HTML files for UI  
│   ├── start.html          # Language selection page  
│   ├── chat.html           # Chat interface                
│── app.py                  # Flask application  
│── requirements.txt        # Dependencies  
│── README.md               # Project documentation  
```

## 🤖 Technologies Used  
- **Python** (Flask, LangChain, OpenAI API)  
- **HTML** (Frontend UI)  
- **SQLite** (User mistake tracking database)  

## 📝 To-Do List  
- [ ] Add voice input/output  
- [ ] Improve AI feedback with more detailed explanations  
- [ ] Support for more languages  

 

## 📄 License  
This project is open-source and available under the MIT License.  

---

### ✨ Start Learning a New Language with LanguageBot Today! 🚀  
