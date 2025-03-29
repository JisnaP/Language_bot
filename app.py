from flask import Flask, request, render_template, session,redirect,url_for
from lang_bot.langbot import LanguageBot,initialize_db
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
os.environ.pop("SSL_CERT_FILE", None) 
@app.route("/", methods=["GET", "POST"])
def start():
    if request.method == "POST":

        session.update({
            "learning_language": request.form.get("learning_language"),
            "known_language": request.form.get("known_language"),
            "level": request.form.get("level"),
            "conversation": []
        })
        bot = LanguageBot(
        session["learning_language"],
        session["known_language"],
        session["level"]
    )
        bot.clear_mistakes()
        return redirect(url_for("chat"))
    return render_template("start.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if not all(key in session for key in ["learning_language", "known_language", "level"]):
        return redirect(url_for("start"))

    if "conversation" not in session:
        session["conversation"] = []

    bot = LanguageBot(
        session["learning_language"],
        session["known_language"],
        session["level"]
    )

    mistakes_summary = ""
    
    if request.method == "POST":
        if "show_mistakes" in request.form:
            mistakes_summary = bot.get_mistakes_summary()
        elif "user_input" in request.form:
            user_input = request.form.get("user_input", "").strip()
            if user_input:
                bot_response = bot.get_response(user_input)
                corrected_input = bot.detect_and_correct(user_input)
                
                # Get the last response which contains the translation
                last_response = bot.conversation_history[-1]
                
                session["conversation"].append({
                    "user": user_input,
                    "corrected": corrected_input,
                    "bot": bot_response,
                    "translation": last_response["translation"]
                })
                session.modified = True

    return render_template("chat.html",
                         conversation=session["conversation"],
                         mistakes_summary=mistakes_summary,
                         learning_language=session["learning_language"],
                         known_language=session["known_language"],
                         level=session["level"])


if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)