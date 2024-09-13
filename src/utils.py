import re
from collections import Counter
from urllib.parse import urlparse


def append_protocol_to_url(url: str) -> str:
    # Strip leading and trailing whitespace
    url = url.strip()

    # Check if the URL already starts with a scheme
    if re.match(r"^https?://", url):
        return url

    # For other cases, try to parse the URL
    parsed = urlparse(url)
    if parsed.netloc:
        # If there's a network location (domain), prepend 'https://'
        return f"https://{url}"
    elif parsed.path and "." in parsed.path:
        # If there's no network location but the path looks like a domain, prepend 'https://'
        return f"https://{url}"
    else:
        # For all other cases, return the original URL
        return url


def analyze_text(text: str, use_nltk: bool = False) -> dict:
    if use_nltk:
        import nltk
        from nltk.corpus import stopwords
        from nltk.tokenize import sent_tokenize, word_tokenize

        nltk.download("stopwords")

        # Tokenize the text
        words = word_tokenize(text.lower())
        sentences = sent_tokenize(text)

        # Remove stopwords and short words
        stop_words = set(stopwords.words("english"))
        interesting_words = [
            word for word in words if word not in stop_words and len(word) > 2
        ]
    else:
        sentences = re.findall(r"\w+[.!?](?:\s|$)", text)
        interesting_words = re.findall(r"\w+", text.lower())

    analysis = {
        "char_count": len(text),
        "newline_count": text.count("\n"),
        "word_count": len(text.split()),
        "sentence_count": len(sentences),
        "paragraph_count": len(text.split("\n\n")),
        "unique_words": len(set(re.findall(r"\w+", text.lower()))),
        "avg_word_length": (
            sum(len(word) for word in text.split()) / len(text.split())
            if text.split()
            else 0
        ),
        "top_10_words": Counter(interesting_words).most_common(10),
    }
    return analysis
