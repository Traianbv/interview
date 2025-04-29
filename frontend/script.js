let currentIndex = 0;
let totalQuestions = 0;
let currentLevel = null;

// Mapping pentru titluri dinamice
const interviewTitles = {
  SOC1: 'SOC Analyst',
  SOC2: 'SOC Analyst Avansat',
  NETADMIN: 'Network Administrator',
  SOFTWAREDEV: 'Software Developer'
};

async function startInterview(level) {
  currentLevel = level;
  currentIndex = 0;
  // Actualizare titlu dinamic
  document.getElementById("interview-title").textContent = `Simulare Interviu ${interviewTitles[level] || ''}`;
  
  // Ascunde selecția nivelului și afișează interviul
  document.getElementById("level-selection").style.display = "none";
  document.getElementById("qa-box").style.display = "block";
  document.getElementById("final-evaluation").style.display = "none";
  
  try {
    // Resetează sesiunea
    await fetch("/reset", {
      method: "POST"
    });
    
    // Setează nivelul în sesiune
    const response = await fetch("/api/set-level", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ level: level })
    });
    
    if (!response.ok) {
      throw new Error("Eroare la setarea nivelului");
    }
    
    // Încarcă prima întrebare
    await loadQuestion();
  } catch (error) {
    console.error("Error starting interview:", error);
    alert("A apărut o eroare la începerea interviului. Te rog să încerci din nou.");
  }
}

async function loadQuestion() {
  try {
    const response = await fetch("/api/question");
    const data = await response.json();
    console.log('[DEBUG] Raspuns primit de la backend /api/question:', data);

    if (data.error) {
      throw new Error(data.error);
    }

    if (data.done) {
      showFinalEvaluation();
      return;
    }

    // Resetăm interfața pentru noua întrebare
    document.getElementById("answer").value = "";
    document.getElementById("feedback").textContent = "";
    document.getElementById("score").textContent = "";
    document.getElementById("next-btn").style.display = "none";
    document.getElementById("correct-answer").style.display = "none";

    // Debug suplimentar: verificăm dacă data.question există
    if (typeof data.question === 'undefined') {
      console.error('[DEBUG] data.question este undefined! Raspuns complet:', data);
      alert('Eroare internă: Răspunsul de la backend nu conține cheia "question".');
      throw new Error('Răspunsul de la backend nu conține cheia "question".');
    }

    // Debug: verificăm existența elementelor în DOM
    const questionElem = document.getElementById("question");
    const counterElem = document.getElementById("question-counter");
    console.log('[DEBUG] questionElem:', questionElem);
    console.log('[DEBUG] counterElem:', counterElem);
    if (!questionElem || !counterElem) {
      alert("Eroare internă: Elementul de întrebare sau contor lipsă în HTML. Verifică structura index.html!");
      throw new Error("Elementul de întrebare sau contor lipsă în HTML");
    }
    // Actualizăm întrebarea și contorul
    questionElem.textContent = data.question;
    counterElem.textContent = `Întrebarea ${data.current_question_index} din ${data.total_questions}`;

    // Dacă este o întrebare follow-up, adăugăm un indicator vizual
    if (data.is_follow_up) {
      const followUpIndicator = document.createElement("div");
      followUpIndicator.className = "follow-up-indicator";
      followUpIndicator.textContent = "Întrebare de clarificare";
      document.getElementById("qa-box").insertBefore(
        followUpIndicator,
        document.getElementById("question")
      );
    }

  } catch (error) {
    console.error("Error loading question:", error);
    alert("A apărut o eroare la încărcarea întrebării. Te rog să încerci din nou.");
  }
}

async function submitAnswer() {
  const answer = document.getElementById("answer").value.trim();
  if (!answer) {
    alert("Te rog să introduci un răspuns.");
    return;
  }

  try {
    const response = await fetch("/api/answer", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ response: answer })
    });

    const data = await response.json();

    // Afișăm feedback-ul și scorul
    document.getElementById("feedback").textContent = data.feedback;
    document.getElementById("score").textContent = `Scor: ${(data.score * 100).toFixed(0)}%`;
    document.getElementById("correct-answer").textContent = `Răspuns recomandat: ${data.correct_answer}`;
    document.getElementById("correct-answer").style.display = "block";

    // Mergem direct la următoarea întrebare, ignorând follow-up
    document.getElementById("next-btn").textContent = "Următoarea întrebare";
    document.getElementById("next-btn").style.display = "block";

  } catch (error) {
    console.error("Error submitting answer:", error);
    alert("A apărut o eroare la trimiterea răspunsului. Te rog să încerci din nou.");
  }
}

async function loadNextQuestion() {
  currentIndex++;
  await loadQuestion();
}

async function showFinalEvaluation() {
  try {
    const res = await fetch("/api/final-evaluation");
    const data = await res.json();

    document.getElementById("qa-box").style.display = "none";
    document.getElementById("final-evaluation").style.display = "block";
    
    document.getElementById("technical-score").textContent = data.technical_score.toFixed(2);
    document.getElementById("soft-skills-score").textContent = data.soft_skills_score.toFixed(2);
    document.getElementById("technical-feedback").textContent = data.technical_feedback;
    document.getElementById("soft-skills-feedback").textContent = data.soft_skills_feedback;
    
    const recommendationsList = document.getElementById("recommendations");
    recommendationsList.innerHTML = "";
    data.recommendations.forEach(rec => {
      const li = document.createElement("li");
      li.textContent = rec;
      recommendationsList.appendChild(li);
    });
  } catch (error) {
    console.error("Error showing final evaluation:", error);
    alert("A apărut o eroare la afișarea evaluării finale. Te rog să încerci din nou.");
  }
}

async function resetInterview() {
  if (confirm("Sigur dorești să resetezi interviul? Vei pierde progresul curent.")) {
    try {
      const res = await fetch("/reset", {
        method: "POST"
      });
      if (res.ok) {
        currentIndex = 0;
        document.getElementById("answer").value = "";
        document.getElementById("feedback").style.display = "none";
        document.getElementById("next-btn").style.display = "none";
        document.getElementById("submit-btn").style.display = "block";
        document.getElementById("qa-box").style.display = "block";
        document.getElementById("final-evaluation").style.display = "none";
        await loadQuestion();
        alert("Interviul a fost resetat cu succes!");
      }
    } catch (error) {
      console.error("Error resetting interview:", error);
      alert("A apărut o eroare la resetarea interviului. Te rog să încerci din nou.");
    }
  }
}

// Funcție pentru ieșirea din interviu și revenirea la pagina principală
async function exitInterview() {
  if (confirm("Sigur dorești să ieși și să te întorci la pagina principală? Progresul va fi pierdut.")) {
    try {
      await fetch("/reset", { method: "POST" });
    } catch (error) {
      console.error("Error resetting session:", error);
    }
    // Resetăm UI și titlu
    document.getElementById("qa-box").style.display = "none";
    document.getElementById("final-evaluation").style.display = "none";
    document.getElementById("level-selection").style.display = "block";
    document.getElementById("interview-title").textContent = "Simulare Interviu";
  }
}