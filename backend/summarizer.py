from transformers import pipeline

# Free summarizer model
summarizer_model = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_reasons(news, tweets):
    combined_text = " ".join([n['title'] for n in news] + tweets)
    if not combined_text.strip():
        return "No relevant information found."
    
    summary = summarizer_model(combined_text, max_length=60, min_length=15, do_sample=False)
    return summary[0]['summary_text']
