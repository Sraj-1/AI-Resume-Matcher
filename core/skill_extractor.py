import re
import logging
from difflib import get_close_matches

logging.basicConfig(level=logging.INFO)

# ================= SKILL DICTIONARY ================= #
# 🔥 Canonical skill → variations
SKILL_DB = {
    # Programming
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "c++": ["c++"],
    "c#": ["c#", "csharp"],

    # Web
    "html": ["html"],
    "css": ["css"],
    "react": ["react", "reactjs"],
    "node": ["node", "nodejs"],
    "express": ["express", "expressjs"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],

    # Data Science
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "scikit-learn": ["scikit learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],

    # Databases
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb"],
    "sqlite": ["sqlite"],
    "nosql": ["nosql"],

    # DevOps / Cloud
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "jenkins": ["jenkins"],
    "git": ["git"],
    "linux": ["linux"]
}


# ================= NORMALIZATION ================= #
def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = text.replace("-", " ").replace(".", " ")
    text = re.sub(r'[^a-z\s#+]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# ================= FUZZY MATCH ================= #
def fuzzy_match(word: str, skill_variations: list, threshold=0.85) -> bool:
    """
    Check if word approximately matches any variation
    """
    matches = get_close_matches(word, skill_variations, n=1, cutoff=threshold)
    return len(matches) > 0


# ================= SKILL EXTRACTION ================= #
def extract_skills(text: str) -> set:
    """
    Extract skills using:
    - Exact match
    - Fuzzy match
    """

    if not text:
        return set()

    text = normalize_text(text)
    tokens = text.split()

    found_skills = set()

    for canonical_skill, variations in SKILL_DB.items():

        # 🔥 Exact phrase match (important for multi-word skills)
        for variation in variations:
            if variation in text:
                found_skills.add(canonical_skill)
                break

        # 🔥 Fuzzy token matching
        for token in tokens:
            if fuzzy_match(token, variations):
                found_skills.add(canonical_skill)
                break

    return found_skills


# ================= SKILL GAP ================= #
def analyze_skill_gap(resume_text: str, jd_text: str):
    """
    Compare resume and JD skills
    """

    try:
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        matched_skills = resume_skills.intersection(jd_skills)
        missing_skills = jd_skills.difference(resume_skills)

        return matched_skills, missing_skills, jd_skills

    except Exception as e:
        logging.error(f"Error in skill analysis: {e}")
        return set(), set(), set()