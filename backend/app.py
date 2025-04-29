from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from evaluator import evaluate_response
from questions import questions
import json
import os
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = 'SOC@2024!Interview#Secret$Key%123'  # Cheie secretă pentru sesiune

# Get the absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "..", "frontend")

# Inițializăm întrebările grupate pe niveluri dinamic pe baza nivelurilor din questions.py
questions_by_level = {
    level: [q for q in questions if q["level"] == level]
    for level in sorted({q["level"] for q in questions})
}

# Serve static files from frontend directory
@app.route("/")
def serve_frontend():
    return send_from_directory(frontend_dir, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(frontend_dir, path)

@app.route("/api/set-level", methods=["POST"])
def set_level():
    try:
        data = request.json
        level = data.get("level")
        
        # Validăm nivelul cerut față de cheile disponibile din questions_by_level
        if level not in questions_by_level:
            return jsonify({"error": "Nivel invalid"})
        
        session["current_level"] = level
        session["score_sum"] = 0.0
        session["answered"] = 0
        session["responses"] = []
        session["level_questions"] = []
        session["follow_up"] = False
        
        return jsonify({"status": "success", "level": level})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Eroare la setarea nivelului: {str(e)}"})

@app.route("/api/question", methods=["GET"])
def get_question():
    try:
        if "current_level" not in session:
            return jsonify({"error": "Nivelul nu a fost selectat"})

        level = session["current_level"]
        pool = questions_by_level.get(level, [])
        print(f"[DEBUG] Nivel selectat: {level}, Pool de întrebări: {pool}")

        if not pool:
            return jsonify({"error": f"Nu există întrebări pentru nivelul {level}"})

        # Verificare structură pool (sanity check)
        for q in pool:
            for key in ["question", "level", "keywords", "answer"]:
                if key not in q:
                    return jsonify({"error": f"Întrebarea din pool nu are cheia obligatorie '{key}': {q}"})
            if "follow_up" in q and q["follow_up"]:
                fu = q["follow_up"]
                if not isinstance(fu, dict):
                    return jsonify({"error": f"Cheia 'follow_up' nu este dict: {q}"})
                for key in ["question", "keywords", "answer"]:
                    if key not in fu:
                        return jsonify({"error": f"Întrebarea follow_up nu are cheia obligatorie '{key}': {fu}"})

        # Verificăm dacă avem o întrebare follow-up activă
        if session.get("follow_up"):
            current_question = session.get("current_question")
            for q in pool:
                if q["question"] == current_question:
                    session["follow_up"] = False  # Resetăm flag-ul după ce am găsit întrebarea
                    return jsonify({
                        "question": current_question,
                        "level": q["level"],
                        "total_questions": len(pool),
                        "current_question_index": len(session["level_questions"]) + 1,
                        "is_follow_up": True
                    })

        # Verificăm dacă am terminat toate întrebările din nivelul curent
        if len(session["level_questions"]) >= len(pool):
            return jsonify({"done": True})

        # Alege o întrebare random din nivelul curent care nu a fost încă răspunsă
        available_questions = [q for q in pool if q["question"] not in session["level_questions"]]
        if not available_questions:
            return jsonify({"done": True})

        question = random.choice(available_questions)
        session["current_question"] = question["question"]

        return jsonify({
            "question": question["question"],
            "level": question["level"],
            "total_questions": len(pool),
            "current_question_index": len(session["level_questions"]) + 1,
            "is_follow_up": False
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Eroare la încărcarea întrebării: {str(e)}"})

@app.route("/api/answer", methods=["POST"])
def post_answer():
    data = request.json
    response = data["response"]
    asked_question = session.get("current_question")

    # Găsește întrebarea curentă pentru evaluare
    question_data = None
    for level, qlist in questions_by_level.items():
        for q in qlist:
            if q["question"] == asked_question:
                question_data = q
                break
        if question_data:
            break

    if not question_data:
        return jsonify({"error": "Întrebarea nu a fost găsită."})

    keywords = question_data["keywords"]
    correct_answer = question_data.get("answer", "")

    # Evaluează răspunsul
    score, feedback = evaluate_response(response, keywords, correct_answer)

    # Stocăm răspunsul pentru evaluarea finală
    session["responses"].append({
        "question": asked_question,
        "response": response,
        "score": score,
        "feedback": feedback,
        "level": question_data["level"]
    })

    # Adăugăm întrebarea la lista celor răspunse în nivelul curent
    if asked_question not in session["level_questions"]:
        session["level_questions"].append(asked_question)

    # Actualizează scorul
    session["score_sum"] += score
    session["answered"] += 1
    avg_score = session["score_sum"] / session["answered"]

    # Trimitere follow-up doar dacă răspuns parțial: unele cuvinte cheie găsite, dar nu răspuns perfect
    if score > 0 and score < 1.0 and isinstance(question_data.get("follow_up"), dict):
        fu = question_data["follow_up"]
        for key in ["question", "keywords", "answer"]:
            if key not in fu:
                return jsonify({"error": f"Întrebarea follow_up nu are cheia obligatorie '{key}': {fu}"})
        follow_up_question = fu
        session["current_question"] = fu["question"]
        session["follow_up"] = True  # Marcăm că urmează o întrebare follow-up

    return jsonify({
        "score": score,
        "average_score": avg_score,
        "feedback": feedback,
        "correct_answer": correct_answer,
        "current_level": session["current_level"],
        "follow_up_question": follow_up_question if 'follow_up_question' in locals() else None
    })

@app.route("/reset", methods=["POST"])
def reset_session():
    session.clear()
    return jsonify({"status": "resetat"})

@app.route("/api/final-evaluation", methods=["GET"])
def get_final_evaluation():
    if "responses" not in session or not session["responses"]:
        return jsonify({"error": "Nu există răspunsuri pentru evaluare"})

    responses = session["responses"]
    
    # Calculăm scorul tehnic
    technical_scores = [r["score"] for r in responses]
    technical_score = sum(technical_scores) / len(technical_scores)
    
    # Calculăm scorul pentru soft skills
    soft_skills_scores = []
    for response in responses:
        # Analizăm feedback-ul pentru a evalua soft skills
        feedback = response["feedback"].lower()
        score = 0.5  # Scor de bază
        
        # Verificăm structura răspunsului
        if "structurat" in feedback or "organizat" in feedback:
            score += 0.2
        if "clar" in feedback or "coerent" in feedback:
            score += 0.2
        if "concis" in feedback or "precis" in feedback:
            score += 0.1
            
        soft_skills_scores.append(score)
    
    soft_skills_score = sum(soft_skills_scores) / len(soft_skills_scores)
    
    # Generăm feedback tehnic
    technical_feedback = "Evaluare tehnică:\n"
    for i, response in enumerate(responses, 1):
        technical_feedback += f"\nÎntrebarea {i}: {response['score']:.2f} - {response['feedback']}"
    
    # Generăm feedback pentru soft skills
    soft_skills_feedback = "Evaluare soft skills:\n"
    if soft_skills_score >= 0.8:
        soft_skills_feedback += "Excelent! Ai demonstrat abilități foarte bune de comunicare și structurare a răspunsurilor."
    elif soft_skills_score >= 0.6:
        soft_skills_feedback += "Bun! Răspunsurile tale sunt în general bine structurate și clare."
    else:
        soft_skills_feedback += "Poți îmbunătăți modul în care structurezi și prezinți răspunsurile."
    
    # Generăm recomandări
    recommendations = []
    
    # Recomandări tehnice
    if technical_score < 0.7:
        recommendations.append("Recomandăm să studiezi mai în profunzime conceptele de bază din SOC.")
    elif technical_score < 0.9:
        recommendations.append("Poți îmbunătăți răspunsurile adăugând mai multe detalii tehnice.")
    
    # Recomandări pentru soft skills
    if soft_skills_score < 0.7:
        recommendations.append("Încearcă să structurezi răspunsurile în mod mai clar și mai organizat.")
    if soft_skills_score < 0.6:
        recommendations.append("Folosește mai multe exemple concrete pentru a ilustra punctele tale.")
    
    # Recomandări generale
    if technical_score >= 0.9 and soft_skills_score >= 0.8:
        recommendations.append("Felicitări! Ai demonstrat cunoștințe tehnice solide și abilități excelente de comunicare.")
    elif technical_score >= 0.7 and soft_skills_score >= 0.7:
        recommendations.append("Continuă să te dezvolți în ambele direcții pentru a deveni un expert în domeniu.")
    
    return jsonify({
        "technical_score": technical_score,
        "soft_skills_score": soft_skills_score,
        "technical_feedback": technical_feedback,
        "soft_skills_feedback": soft_skills_feedback,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)