export function renderResults(list = []) {
  const container = document.querySelector("#resultsContainer")
  container.innerHTML = ""

  list.forEach((c) => {
    const div = document.createElement("div")
    div.className = "card result-card"

    div.innerHTML = `
      <div class="rank">#${c.rank}</div>
      <h3>${c.name}</h3>
      <p><b>Role:</b> ${c.role}</p>
      <p><b>Experience:</b> ${c.experience}</p>

      <div class="scores">
        <span>Match: ${c.match_score}</span>
        <span>Engagement: ${c.engagement_score}</span>
        <span>Final: ${c.final_score}</span>
      </div>

      <div class="skills">
        ${(c.top_skills || []).map(s => `<span>${s}</span>`).join("")}
      </div>
    `

    container.appendChild(div)
  })
}