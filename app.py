from flask import Flask, request, render_template
from transformers import pipeline

app = Flask(__name__)

# Load summarization model
summarizer = pipeline("summarization")

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    if request.method == 'POST':
        text = request.form['text']
        if len(text.split()) > 3000:
            summary = "Error: The input text exceeds 3000 words. Please enter a shorter text."
        else:
            # Split text into chunks to handle long inputs
            max_chunk_size = 1000
            chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
            summarized_chunks = []
            for chunk in chunks:
                summarized_chunk = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
                summarized_chunks.append(summarized_chunk)
            summary = ' '.join(summarized_chunks)
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
