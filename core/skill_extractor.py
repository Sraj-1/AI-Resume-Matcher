import re
import logging

logging.basicConfig(level=logging.INFO)

# 🔥 Comprehensive skill set (can expand later)
TECH_SKILLS = {
    # Programming Languages
    "python", "java", "javascript", "c++", "c#", "go", "ruby",

    # Web Development
    "html", "css", "react", "node", "express", "django", "flask", "fastapi",

    # Data Science / ML
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch",
    "scikit learn", "pandas", "numpy", "matplotlib",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "nosql",

    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "linux"
}


def normalize_text(text: str) -> str:
    """
    Normalize text for better matching
    """
    text = text.lower()
    text = text.replace("-", " ").replace(".", " ")
    return text


def extract_skills(text: str) -> set:
    """
    Extract skills from text using keyword matching.
    
    Args:
        text (str): Cleaned text
    
    Returns:
        set: Found skills
    """

    if not text:
        return set()

    text = normalize_text(text)
    found_skills = set()

    for skill in TECH_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)

    return found_skills


def analyze_skill_gap(resume_text: str, jd_text: str):
    """
    Compare resume and JD skills.
    
    Returns:
        matched_skills, missing_skills, jd_skills
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