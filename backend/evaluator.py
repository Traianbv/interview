def evaluate_response(response, keywords, correct_answer=None):
    # Normalizează ambele răspunsuri pentru comparație
    normalized_response = ' '.join(response.lower().strip().split())
    normalized_correct = ' '.join(correct_answer.lower().strip().split()) if correct_answer else ""
    
    # Verifică dacă răspunsul este identic cu cel recomandat
    if correct_answer and normalized_response == normalized_correct:
        return 1.0, "Răspuns perfect! Exact ca cel recomandat."

    # Verifică cuvintele cheie
    total = len(keywords)
    found = sum(1 for k in keywords if k.lower() in normalized_response)
    score = found / total if total > 0 else 0.0

    # Generează feedback bazat pe scor
    if score == 1:
        feedback = "Răspuns complet și bine structurat."
    elif score >= 0.7:
        feedback = "Răspuns bun, dar poți adăuga mai multe detalii."
    elif score >= 0.5:
        feedback = "Răspuns parțial. Încearcă să oferi mai multe detalii."
    elif score >= 0.3:
        feedback = "Răspuns slab. Revizuiește conceptele de bază."
    else:
        feedback = "Răspunsul nu acoperă conceptele cheie. Revizuiește materialul."

    return score, feedback

def generate_final_evaluation(responses):
    if not responses:
        return {
            "technical_score": 0,
            "soft_skills_score": 0,
            "technical_feedback": "Nu există răspunsuri pentru evaluare",
            "soft_skills_feedback": "Nu există răspunsuri pentru evaluare",
            "recommendations": []
        }

    # Calculăm scorul tehnic
    technical_scores = [r["score"] for r in responses]
    technical_score = sum(technical_scores) / len(technical_scores)

    # Analizăm soft skill-urile
    soft_skills_indicators = {
        "comunicare": ["clar", "structurat", "coerent", "explicat"],
        "analiză": ["detaliat", "complet", "exhaustiv", "sistematic"],
        "confidență": ["sigur", "precis", "concis", "direct"],
        "adaptabilitate": ["flexibil", "versatil", "divers", "complet"]
    }

    soft_skills_scores = {skill: 0 for skill in soft_skills_indicators}
    total_indicators = sum(len(indicators) for indicators in soft_skills_indicators.values())

    for response in responses:
        text = response["response"].lower()
        for skill, indicators in soft_skills_indicators.items():
            matches = sum(1 for indicator in indicators if indicator in text)
            soft_skills_scores[skill] += matches / len(indicators)

    # Normalizăm scorurile soft skills
    for skill in soft_skills_scores:
        soft_skills_scores[skill] = soft_skills_scores[skill] / len(responses)

    soft_skills_score = sum(soft_skills_scores.values()) / len(soft_skills_scores)

    # Generăm feedback tehnic
    if technical_score >= 0.9:
        technical_feedback = "Excelentă înțelegere a conceptelor tehnice. Demonstrează cunoștințe solide în domeniu."
    elif technical_score >= 0.7:
        technical_feedback = "Bună înțelegere a conceptelor tehnice. Unele aspecte pot fi îmbunătățite."
    elif technical_score >= 0.5:
        technical_feedback = "Înțelegere medie a conceptelor tehnice. Recomand revizuirea materialului."
    else:
        technical_feedback = "Necesită îmbunătățirea cunoștințelor tehnice. Recomand studiu suplimentar."

    # Generăm feedback pentru soft skills
    soft_skills_feedback = []
    for skill, score in soft_skills_scores.items():
        if score >= 0.8:
            soft_skills_feedback.append(f"Excelentă {skill}.")
        elif score >= 0.6:
            soft_skills_feedback.append(f"Bună {skill}.")
        elif score >= 0.4:
            soft_skills_feedback.append(f"{skill.capitalize()} medie.")
        else:
            soft_skills_feedback.append(f"Necesită îmbunătățirea {skill}.")

    # Generăm recomandări
    recommendations = []
    if technical_score < 0.7:
        recommendations.append("Revizuirea conceptelor tehnice de bază")
    if soft_skills_score < 0.7:
        recommendations.append("Dezvoltarea abilităților de comunicare și prezentare")
    if technical_score >= 0.9 and soft_skills_score >= 0.9:
        recommendations.append("Pregătire pentru nivelul următor de complexitate")
    else:
        recommendations.append("Exersarea răspunsurilor pentru a fi mai concise și structurate")

    return {
        "technical_score": round(technical_score, 2),
        "soft_skills_score": round(soft_skills_score, 2),
        "technical_feedback": technical_feedback,
        "soft_skills_feedback": " ".join(soft_skills_feedback),
        "recommendations": recommendations
    }