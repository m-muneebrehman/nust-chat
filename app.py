from flask import Flask, render_template, request, jsonify
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# Load resources at startup
print("Loading index and chunks...")
index = faiss.read_index("index.faiss")
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Ready.")

# Threshold – adjust as needed
SCORE_THRESHOLD = 1.071

def get_answer(query):
    q_emb = model.encode([query])
    distances, indices = index.search(np.array(q_emb), 1)
    dist = distances[0][0]
    idx = indices[0][0]
    chunk = chunks[idx]

    if dist <= SCORE_THRESHOLD:
        if "\nA: " in chunk:
            _, answer = chunk.split("\nA: ", 1)
        else:
            answer = chunk
        return answer.strip()
    else:
        return "I don't know. Please ask about admissions, fees, eligibility, etc."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    answer = get_answer(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)