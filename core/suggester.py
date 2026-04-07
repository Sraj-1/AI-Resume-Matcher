def generate_suggestions(match_score: float, missing_skills: set) -> list:
    """
    Generate intelligent suggestions based on match score and skill gaps.

    Args:
        match_score (float): Match score (0–100)
        missing_skills (set): Skills missing from resume

    Returns:
        list: List of suggestions
    """

    suggestions = []

    # 🎯 Score-based suggestions
    if match_score >= 80:
        suggestions.append("🌟 Excellent match! Your resume is highly aligned with this role. Focus on interview preparation.")
    elif match_score >= 60:
        suggestions.append("👍 Good match, but you can improve by aligning your resume more closely with the job description.")
    elif match_score >= 40:
        suggestions.append("⚠️ Average match. Consider improving your resume by adding relevant skills and projects.")
    else:
        suggestions.append("❌ Low match. You should significantly improve your resume or consider roles better aligned with your skills.")

    # 🛠️ Skill-based suggestions
    if missing_skills:
        top_missing = list(missing_skills)[:5]  # limit for readability
        suggestions.append(
            f"💡 You are missing important skills: {', '.join(top_missing)}. Consider learning or adding them."
        )
        suggestions.append(
            "📚 Add relevant projects or certifications to demonstrate these skills."
        )
    else:
        suggestions.append("🎯 Great! You have all the key skills required for this role.")

    # ✨ General resume improvement tips
    suggestions.append("📝 Use strong action verbs and quantify your achievements (e.g., 'improved accuracy by 20%').")
    suggestions.append("📄 Keep your resume concise (1–2 pages) and tailored for each job.")

    return suggestions