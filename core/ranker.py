import logging
from utils.extractor import extract_text_from_pdf
from utils.preprocessor import clean_text
from core.matcher import calculate_match_score

logging.basicConfig(level=logging.INFO)


def rank_resumes(uploaded_files, jd_text: str, use_bert: bool = False):
    """
    Rank multiple resumes based on match score

    Returns:
        list of dicts → [{name, score}]
    """

    results = []

    if not jd_text.strip():
        return results

    clean_jd = clean_text(jd_text)

    for file in uploaded_files:
        try:
            # Extract
            raw_text = extract_text_from_pdf(file)

            if not raw_text:
                continue

            # Clean
            clean_resume = clean_text(raw_text)

            # Score
            score = calculate_match_score(clean_resume, clean_jd, use_bert=use_bert)

            results.append({
                "name": file.name,
                "score": score
            })

        except Exception as e:
            logging.error(f"Error processing {file.name}: {e}")

    # Sort (highest first)
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results