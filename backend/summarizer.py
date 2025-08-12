# backend/summarizer.py
# simple extractive summarizer using sentence scoring by word frequency
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import math

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))


def summarize_text(text: str, max_sentences: int = 3) -> str:
    if not text:
        return ""
    sentences = sent_tokenize(text)
    if len(sentences) <= max_sentences:
        return text

    # build frequency table
    freq = {}
    for sent in sentences:
        for w in word_tokenize(sent.lower()):
            if w.isalpha() and w not in stop_words:
                freq[w] = freq.get(w, 0) + 1

    # score sentences
    scores = []
    for sent in sentences:
        s = 0
        words = [w for w in word_tokenize(sent.lower()) if w.isalpha()]
        for w in words:
            s += freq.get(w, 0)
        # normalize by sentence length
        if len(words) > 0:
            scores.append((s / math.sqrt(len(words)), sent))
        else:
            scores.append((0, sent))

    # pick top sentences
    scores.sort(key=lambda x: x[0], reverse=True)
    top = sorted(scores[:max_sentences], key=lambda x: sentences.index(x[1]))
    summary = " ".join([t[1] for t in top])
    return summary


if __name__ == "__main__":
    txt = ("Infosys reported its quarterly results... " * 4)
    print(summarize_text(txt))