const TOOLS = {
  qa: {
    label: "Ask a question", desc: "Quick, accurate answers",
    endpoint: "/qa", button: "Get answer",
    hint: "Ask anything from your syllabus or general knowledge.",
    placeholder: "Which is the largest ocean?"
  },
  explain: {
    label: "Explain a concept", desc: "Plain-language breakdowns",
    endpoint: "/explain", button: "Explain it",
    hint: "Type a concept and get a simple explanation with an example.",
    placeholder: "Recursion in programming"
  },
  quiz: {
    label: "Generate a quiz", desc: "3 questions to test yourself",
    endpoint: "/quiz", button: "Generate quiz",
    hint: "Enter a topic or paste a passage. You get 3 multiple-choice questions.",
    placeholder: "The Pythagoras theorem"
  },
  summarize: {
    label: "Summarize text", desc: "Long passages, short notes",
    endpoint: "/summarize", button: "Summarize",
    hint: "Paste a long paragraph and get the key points for revision.",
    placeholder: "Paste the passage you want summarized..."
  },
  learn: {
    label: "Learning path", desc: "Beginner to advanced plan",
    endpoint: "/learn/recommendations", button: "Build my path",
    hint: "Name a subject and pick your level to get a step-by-step plan.",
    placeholder: "SQL"
  }
};

let current = "qa";
const $ = (id) => document.getElementById(id);
const input = $("input"), submit = $("submit"), result = $("result");

function buildNav() {
  const nav = $("tools");
  Object.entries(TOOLS).forEach(([key, t]) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "tool";
    b.dataset.key = key;
    b.setAttribute("role", "tab");
    b.innerHTML = `<span class="tool-name">${t.label}</span><span class="tool-desc">${t.desc}</span>`;
    b.addEventListener("click", () => selectTool(key));
    nav.appendChild(b);
  });
}

function selectTool(key) {
  current = key;
  const t = TOOLS[key];
  document.querySelectorAll(".tool").forEach((b) => {
    const on = b.dataset.key === key;
    b.classList.toggle("active", on);
    b.setAttribute("aria-selected", on);
  });
  $("tool-title").textContent = t.label;
  $("tool-hint").textContent = t.hint;
  input.placeholder = t.placeholder;
  submit.textContent = t.button;
  $("level-wrap").hidden = key !== "learn";
  input.value = "";
  result.hidden = true;
  result.innerHTML = "";
}

function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function inline(s) {
  return s
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/`(.+?)`/g, "<code>$1</code>");
}

// Tiny Markdown renderer: headings, bullet lists, bold, inline code, paragraphs.
function renderMarkdown(md) {
  const lines = escapeHtml(md).split("\n");
  let html = "", inList = false;
  const closeList = () => { if (inList) { html += "</ul>"; inList = false; } };
  for (const raw of lines) {
    const line = raw.trim();
    let m;
    if (!line) { closeList(); continue; }
    if ((m = line.match(/^(#{1,4})\s+(.*)/))) {
      closeList();
      const lvl = Math.min(m[1].length + 1, 4);
      html += `<h${lvl}>${inline(m[2])}</h${lvl}>`;
    } else if ((m = line.match(/^[-*•]\s+(.*)/)) || (m = line.match(/^\d+[.)]\s+(.*)/))) {
      if (!inList) { html += "<ul>"; inList = true; }
      html += `<li>${inline(m[1])}</li>`;
    } else {
      closeList();
      html += `<p>${inline(line)}</p>`;
    }
  }
  closeList();
  return html;
}

function showText(text) {
  result.innerHTML = renderMarkdown(text);
}

function showError(message) {
  result.innerHTML = `<p class="error">${escapeHtml(message)}</p>`;
}

function showQuiz(questions) {
  let answered = 0, correct = 0;
  result.innerHTML = "";
  questions.forEach((q, qi) => {
    const box = document.createElement("div");
    box.className = "question";
    const h = document.createElement("h3");
    h.textContent = `${qi + 1}. ${q.question}`;
    box.appendChild(h);
    const feedback = document.createElement("p");
    feedback.className = "feedback";
    const buttons = q.options.map((opt, oi) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "option";
      b.textContent = opt;
      b.addEventListener("click", () => {
        buttons.forEach((x) => (x.disabled = true));
        answered++;
        if (oi === q.answer_index) {
          b.classList.add("right");
          feedback.textContent = "Correct.";
          correct++;
        } else {
          b.classList.add("wrong");
          buttons[q.answer_index].classList.add("right");
          feedback.textContent = `Not quite. The correct answer is: ${q.options[q.answer_index]}`;
        }
        if (answered === questions.length) {
          score.textContent = `You scored ${correct} out of ${questions.length}.`;
        }
      });
      box.appendChild(b);
      return b;
    });
    box.appendChild(feedback);
    result.appendChild(box);
  });
  const score = document.createElement("p");
  score.className = "score";
  result.appendChild(score);
}

async function run() {
  const text = input.value.trim();
  if (text.length < 2) {
    result.hidden = false;
    showError("Enter a topic, question or passage first.");
    return;
  }
  const tool = TOOLS[current];
  submit.disabled = true;
  submit.textContent = "Working...";
  result.hidden = false;
  result.innerHTML = '<p class="loading">Asking Gemini...</p>';
  try {
    const res = await fetch(tool.endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, level: $("level").value })
    });
    const data = await res.json();
    if (!res.ok) {
      const detail = Array.isArray(data.detail) ? "Please check your input length." : data.detail;
      throw new Error(detail || "Something went wrong.");
    }
    if (data.questions) showQuiz(data.questions);
    else showText(data.result);
  } catch (err) {
    showError(err.message || "Could not reach the server.");
  } finally {
    submit.disabled = false;
    submit.textContent = tool.button;
  }
}

submit.addEventListener("click", run);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) run();
});
buildNav();
selectTool("qa");
