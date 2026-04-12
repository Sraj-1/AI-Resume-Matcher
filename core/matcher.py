import os
import logging
import joblib
from typing import Tuple, List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from utils.preprocessor import clean_text
from core.skill_extractor import extract_skills

logging.basicConfig(level=logging.INFO)

# ================= PATHS ================= #
MODEL_DIR = "models"
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")

# ================= GLOBAL MODELS ================= #
bert_model = None
tfidf_vectorizer = None


# ================= BERT ================= #
def load_bert():
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
def train_tfidf(corpus: List[str]):
    global tfidf_vectorizer

    try:
        os.makedirs(MODEL_DIR, exist_ok=True)

        tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000
        )

        tfidf_vectorizer.fit(corpus)

        joblib.dump(tfidf_vectorizer, VECTORIZER_PATH)
        logging.info("TF-IDF trained & saved")

    except Exception as e:
        logging.error(f"TF-IDF training error: {e}")


def load_tfidf():
    global tfidf_vectorizer

    if tfidf_vectorizer is None:
        try:
            if os.path.exists(VECTORIZER_PATH):
                tfidf_vectorizer = joblib.load(VECTORIZER_PATH)
                logging.info("TF-IDF loaded")
            else:
                logging.warning("TF-IDF not found. Train first.")
        except Exception as e:
            logging.error(f"TF-IDF loading error: {e}")

    return tfidf_vectorizer


def tfidf_match(resume_text: str, jd_text: str) -> Tuple[float, List[str]]:
    try:
        vectorizer = load_tfidf()

        if vectorizer is None:
            return 0.0, []

        vectors = vectorizer.transform([resume_text, jd_text])

        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

        # 🔥 Keyword explainability
        feature_names = vectorizer.get_feature_names_out()
        resume_vec = vectors[0].toarray()[0]
        jd_vec = vectors[1].toarray()[0]

        overlap = resume_vec * jd_vec
        top_indices = overlap.argsort()[-10:][::-1]

        keywords = [
            feature_names[i]
            for i in top_indices
            if overlap[i] > 0
        ]

        return round(score * 100, 2), keywords

    except Exception as e:
        logging.error(f"TF-IDF error: {e}")
        return 0.0, []


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


# ================= HYBRID SYSTEM ================= #
def calculate_hybrid_score(resume_text: str, jd_text: str) -> Dict:
    """
    FINAL INDUSTRY HYBRID SYSTEM
    """

    if not resume_text or not jd_text:
        return {
            "final_score": 0.0,
            "tfidf": 0.0,
            "bert": 0.0,
            "skill": 0.0,
            "keywords": []
        }

    # 🔥 Preprocessing
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(jd_text)

    # ===== TF-IDF ===== #
    tfidf_score, keywords = tfidf_match(clean_resume, clean_jd)

    # ===== BERT ===== #
    bert_score = bert_match(clean_resume, clean_jd)

    # ===== SKILLS ===== #
    resume_skills = extract_skills(clean_resume)
    jd_skills = extract_skills(clean_jd)

    if jd_skills:
        skill_score = (len(resume_skills & jd_skills) / len(jd_skills)) * 100
    else:
        skill_score = 0.0

    # ===== FINAL SCORE ===== #
    final_score = (
        0.5 * tfidf_score +
        0.3 * bert_score +
        0.2 * skill_score
    )

    return {
        "final_score": round(final_score, 2),
        "tfidf": round(tfidf_score, 2),
        "bert": round(bert_score, 2),
        "skill": round(skill_score, 2),
        "keywords": keywords
    }