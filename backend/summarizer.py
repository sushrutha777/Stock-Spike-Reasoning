from transformers import pipeline

# Load Hugging Face summarizer model (free & local)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_reason(stock, news, tweets):
    text = f"Stock: {stock}\nNews: {', '.join(news)}\nTweets: {', '.join(tweets)}"
    if len(text.split()) < 50:
        return "Not enough data to generate a meaningful summary."
    try:
        summary = summarizer(text, max_length=60, min_length=25, do_sample=False)
        return summary[0]['summary_text']
    except:
        return "Error generating summary."
