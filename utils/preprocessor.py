import spacy
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load spaCy model safely
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except:
        logging.warning("Downloading spaCy model...")
        import os
        os.system("python -m spacy download en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

# 🔥 Custom stopwords (resume-specific noise)
CUSTOM_STOPWORDS = {
    "linkedin", "gmail", "github", "com", "www",
    "mobile", "email", "phone"
}

def clean_text(text: str) -> str:
    """
    Clean and preprocess text using NLP techniques.

    Steps:
    - Lowercasing
    - Remove URLs & emails
    - Remove special characters
    - Tokenization
    - Stopword removal (default + custom)
    - Lemmatization
    """

    if not text or not text.strip():
        return ""

    try:
        # 🔹 Lowercase
        text = text.lower()

        # 🔥 Remove URLs
        text = re.sub(r'http\S+|www\S+', ' ', text)

        # 🔥 Remove emails
        text = re.sub(r'\S+@\S+', ' ', text)

        # 🔹 Remove special characters & numbers
        text = re.sub(r'[^a-z\s]', ' ', text)

        # 🔹 Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()

        # 🔹 Process with spaCy
        doc = nlp(text)

        # 🔥 Clean tokens (important logic)
        cleaned_tokens = []

        for token in doc:
            if (
                not token.is_stop and          # remove default stopwords
                not token.is_punct and         # remove punctuation
                len(token.text) > 2 and        # remove small words
                token.text not in CUSTOM_STOPWORDS  # remove custom noise
            ):
                cleaned_tokens.append(token.lemma_)

        return " ".join(cleaned_tokens)

    except Exception as e:
        logging.error(f"Error in preprocessing: {e}")
        return ""