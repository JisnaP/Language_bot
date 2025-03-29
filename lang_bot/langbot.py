import httpx
from langchain_openai.chat_models import ChatOpenAI

from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()
import sqlite3
import os
os.environ.pop("SSL_CERT_FILE", None) 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class LanguageBot:
    def __init__(self, learning_language, known_language, level):
        self.learning_language = learning_language
        self.known_language = known_language
        self.level = level
        self.chat_model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
        self.conversation_history = []
        self.initialize_db()
    def get_response(self, user_input):
        """Generate a single response to user input"""
        self.conversation_history.append({"role": "user", "content": user_input})
    
        prompt = self._generate_prompt()
        ai_response = self.chat_model.invoke(prompt).content
    
   
        if "Student:" in ai_response:
           ai_response = ai_response.split("Student:")[0].strip()
    
        self.conversation_history.append({
                "role": "assistant",
                "content": ai_response,
                "translation": self._generate_translation(ai_response)
    })
    
        return ai_response    
   
    def _generate_translation(self, text):
        """Generate translation to known language if needed"""
        translation_prompt = f"""
        Translate this {self.learning_language} text to {self.known_language}:
        {text}
        Translation: """
    
        return self.chat_model.invoke(translation_prompt).content.strip()

    def _generate_prompt(self):
        prompt_lines = [self._get_initial_instructions()]
        for msg in self.conversation_history:
            prefix = "Student" if msg["role"] == "user" else "Teacher"
            prompt_lines.append(f"{prefix}: {msg['content']}")
        return "\n".join(prompt_lines)
    def _get_initial_instructions(self):
         return f"""You are a {self.learning_language} teacher for {self.known_language} speakers.
    Teaching Approach:
    1. NATURAL CONVERSATION FIRST:
       - Respond conversationally
       - Embed teaching within dialogue
       - Never show raw lists or metadata
    
    2. STRUCTURED TEACHING:
       - Introduce ONE concept per exchange   
    
    3. TOPIC FLOW:
       - Continue current topic for 3-5 exchanges
       - Then naturally transition
       - Never announce topic changes
    
    4. FORMATTING RULES:
       - Only show conversation text
       - Never show instructions or goals
       - Keep target language prominent
       - Translations in parentheses
    
    Example GOOD response:
    "Try saying 'Good morning' - 'സുപ്രഭാതം' (suprabhātham)"
    
    Example BAD response:
    "Learning Goal: Greetings. Related Phrases: 1. Good morning - സുപ്രഭാതം"
    
    Current priority: Teach practical {self.learning_language} through natural conversation."""
    
    def initialize_db(self):
        conn = sqlite3.connect("mistakes.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mistakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                correction TEXT,
                mistake_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def detect_and_correct(self, user_input):
        correction_prompt = f"""
        Correct this {self.learning_language} sentence from a {self.level} learner who knows {self.known_language}.
        Provide JUST the corrected version with no additional explanation:
        
        Original: {user_input}
        Correction: """
        
        correction = self.chat_model.invoke(correction_prompt).content.strip()
        
        if correction.lower() != user_input.lower():
            self.store_mistake(user_input, correction)
        
        return correction

    def store_mistake(self, user_input, correction):
        type_prompt = f"""
        Classify the language mistake type (grammar, vocabulary, spelling, word order, other):
        Original: {user_input}
        Corrected: {correction}
        Mistake Type: """
        
        mistake_type = self.chat_model.invoke(type_prompt).content.strip()
        
        conn = sqlite3.connect("mistakes.db")
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO mistakes (user_input, correction, mistake_type) VALUES (?, ?, ?)",
                (user_input, correction, mistake_type)
            )
            conn.commit()
        finally:
            conn.close()

    def get_mistakes_summary(self):
        conn = sqlite3.connect("mistakes.db")
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT mistake_type, COUNT(*) as count 
                FROM mistakes 
                GROUP BY mistake_type 
                ORDER BY count DESC
            """)
            stats = cursor.fetchall()
            
            cursor.execute("""
                SELECT user_input, correction, mistake_type 
                FROM mistakes 
                ORDER BY timestamp DESC 
                LIMIT 10
            """)
            recent = cursor.fetchall()
            
            report = "=== Language Learning Report ===\n\n"
            report += "Mistake Statistics:\n"
            for mistake_type, count in stats:
                report += f"- {mistake_type}: {count} errors\n"
            
            report += "\nRecent Mistakes:\n"
            for original, corrected, m_type in recent:
                report += f"Original: {original}\nCorrected: {corrected}\nType: {m_type}\n\n"
            
            return report
        finally:
            conn.close()
    def clear_mistakes(self):
        """Clear all mistakes from the database"""
        conn = sqlite3.connect("mistakes.db")
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mistakes")
            conn.commit()
        finally:
            conn.close()
def initialize_db():
    LanguageBot("English", "Spanish", "Beginner").initialize_db()

