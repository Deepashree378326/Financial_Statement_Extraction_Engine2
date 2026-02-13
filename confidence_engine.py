def calculate_confidence(exact_match, synonym_match, numeric_count):
    score = 0

    if exact_match:
        score += 2
    elif synonym_match:
        score += 1

    if numeric_count > 0:
        score += 2

    if numeric_count > 1:
        score += 1

    if numeric_count == 0:
        score -= 2

    if score >= 5:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"
