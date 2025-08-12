"""
Simple extractive summarizer using sentence scoring by word frequency.
"""
from typing import List
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import math

# try to quiet-download; README instructs to pre-download
try:
    nltk.data.find("tokenizers/punkt")
except Exception:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except Exception:
    nltk.download("stopwords", quiet=True)

stop_words = set(stopwords.words("english"))


def summarize_text(text: str, max_sentences: int = 3) -> str:
    if not text or not text.strip():
        return ""

    sentences = sent_tokenize(text)
    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    freq = {}
    for sent in sentences:
        for w in word_tokenize(sent.lower()):
            if w.isalpha() and w not in stop_words:
                freq[w] = freq.get(w, 0) + 1

    scores = []
    for sent in sentences:
        s = 0
        words = [w for w in word_tokenize(sent.lower()) if w.isalpha()]
        for w in words:
            s += freq.get(w, 0)
        if len(words) > 0:
            scores.append((s / math.sqrt(len(words)), sent))
        else:
            scores.append((0, sent))

    scores.sort(key=lambda x: x[0], reverse=True)
    top = sorted(scores[:max_sentences], key=lambda x: sentences.index(x[1]))
    summary = " ".join([t[1] for t in top])
    return summary