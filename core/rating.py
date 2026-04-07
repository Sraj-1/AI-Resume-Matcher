def get_match_rating(score: float) -> str:
    """
    Convert match score into a human-readable rating.
    
    Args:
        score (float): Match score (0–100)
    
    Returns:
        str: Rating label
    """

    if score >= 80:
        return "Excellent 🔥"
    elif score >= 60:
        return "Good 👍"
    elif score >= 40:
        return "Average ⚠️"
    else:
        return "Poor ❌"