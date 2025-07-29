from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


faq_knowledge = [
    {"question": "What are your business hours?", "answer": "We're open Monday to Friday, 9am to 5pm."},
    {"question": "How do I contact support?", "answer": "You can email us at support@example.com."},
    {"question": "Where are you located?", "answer": "Our headquarters is in San Francisco, California."}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form['question']
    
  
    for item in faq_knowledge:
        if item['question'].lower() == user_question.lower():
            return jsonify({'answer': item['answer']})
    
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful FAQ assistant. Answer questions based on the provided knowledge. If you don't know, say 'I don't have information about that.'"},
                {"role": "user", "content": f"FAQ Knowledge: {str(faq_knowledge)}\n\nQuestion: {user_question}\nAnswer:"}
            ],
            temperature=0.3
        )
        answer = response.choices[0].message.content
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'answer': f"Sorry, I encountered an error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)