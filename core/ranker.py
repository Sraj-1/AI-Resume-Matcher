import logging
from utils.extractor import extract_text_from_pdf
from core.matcher import calculate_hybrid_score

logging.basicConfig(level=logging.INFO)


def rank_resumes(uploaded_files, jd_text: str):
    results = []

    if not jd_text or not jd_text.strip():
        return results

    for file in uploaded_files:
        try:
            raw_text = extract_text_from_pdf(file)

            if not raw_text:
                continue

            result = calculate_hybrid_score(raw_text, jd_text)

            results.append({
                "name": file.name,
                "score": result["final_score"],
                "details": result
            })

        except Exception as e:
            logging.error(f"Error processing {file.name}: {e}")

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results