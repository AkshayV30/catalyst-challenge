export function renderResults(list = []) {
  const container = document.querySelector("#results")
  container.innerHTML = ""

  list.forEach((c) => {
    const el = document.createElement("div")
    el.className = "card result-card"

    el.innerHTML = `
      <div class="rank">#${c.rank}</div>
      <h3>${c.name}</h3>
      <p>${c.role}</p>

      <div class="scores">
        <span>Match: ${c.match_score}</span>
        <span>Engagement: ${c.engagement_score}</span>
        <span>Final: ${c.final_score}</span>
      </div>

      <div class="skills">
        ${(c.top_skills || []).map(s => `<span>${s}</span>`).join("")}
      </div>
    `

    container.appendChild(el)
  })
}