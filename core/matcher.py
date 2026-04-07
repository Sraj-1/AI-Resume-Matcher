from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO)

# ================= GLOBAL MODEL ================= #
bert_model = None


def load_bert():
    """
    Loads BERT model only once (lazy loading)
    """
    global bert_model
    if bert_model is None:
        try:
            logging.info("Loading BERT model...")
            bert_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logging.error(f"BERT loading failed: {e}")
            bert_model = None
    return bert_model


# ================= TF-IDF ================= #
def tfidf_match(resume_text: str, jd_text: str) -> float:
    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(score * 100, 2)
    except Exception as e:
        logging.error(f"TF-IDF error: {e}")
        return 0.0


# ================= BERT ================= #
def bert_match(resume_text: str, jd_text: str) -> float:
    try:
        model = load_bert()

        if model is None:
            return 0.0

        embeddings = model.encode([resume_text, jd_text])
        score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

        return round(score * 100, 2)

    except Exception as e:
        logging.error(f"BERT error: {e}")
        return 0.0


# ================= MAIN FUNCTION ================= #
def calculate_match_score(resume_text: str, jd_text: str, use_bert: bool = False) -> float:
    """
    Hybrid match system

    use_bert = False → TF-IDF
    use_bert = True → BERT
    """

    if not resume_text or not jd_text:
        return 0.0

    if use_bert:
        return bert_match(resume_text, jd_text)
    else:
        return tfidf_match(resume_text, jd_text)