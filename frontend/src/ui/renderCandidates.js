export function renderCandidates(list, containerId) {
  const container = document.querySelector(containerId)
  if (!container) return

  container.innerHTML = ""

  if (!list?.length) {
    container.innerHTML = `<p>No candidates found</p>`
    return
  }

  const fragment = document.createDocumentFragment()

  list.forEach((c) => {
    const el = document.createElement("div")
    el.className = "card result-card"

    el.innerHTML = `
      <div class="rank">#${c.rank ?? "-"}</div>

      <h3>${c.name ?? "Unknown"}</h3>
      <p><b>Role:</b> ${c.role ?? "-"}</p>
      <p><b>Experience:</b> ${c.experience ?? "-"}</p>

      <div class="scores">
        <span>Match: ${c.match_score ?? 0}</span>
        <span>Engagement: ${c.engagement_score ?? 0}</span>
        <span>Final: ${c.final_score ?? 0}</span>
      </div>

      <div class="skills">
        ${(c.top_skills || [])
          .map((s) => `<span>${s}</span>`)
          .join("")}
      </div>
    `

    fragment.appendChild(el)
  })

  container.appendChild(fragment)
}