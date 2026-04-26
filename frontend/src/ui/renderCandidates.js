function createCandidateCard(c) {
  const div = document.createElement("div")
  div.className = "card result-card"

  div.innerHTML = `
    <div class="rank">#${c.rank ?? "-"}</div>

    <h3>${c.name ?? "Unknown"}</h3>
    <p><b>Role:</b> ${c.role ?? "-"}</p>

    <div class="scores">
      <span>Match: ${safeNum(c.match_score)}</span>
      <span>Engagement: ${safeNum(c.engagement_score)}</span>
      <span>Final: ${safeNum(c.final_score)}</span>
    </div>

    <div class="skills">
      ${(c.top_skills ?? [])
        .map(s => `<span>${s}</span>`)
        .join("")}
    </div>
  `

  return div
}

function safeNum(v) {
  if (v === null || v === undefined || isNaN(v)) return 0
  return Number(v).toFixed ? Number(v).toFixed(2) : v
}

export function renderCandidates(list = [], container) {
  if (!container) return

  container.innerHTML = ""

  const fragment = document.createDocumentFragment()

  for (const c of list) {
    fragment.appendChild(createCandidateCard(c))
  }

  container.appendChild(fragment)
}

export function appendCandidate(candidate, container) {
  if (!container) return
  container.appendChild(createCandidateCard(candidate))
}