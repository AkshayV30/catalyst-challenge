import { create } from "../utils/dom"
import { safe } from "../utils/format"

export function CandidateCard(c) {
  const el = create("div", "card")

  el.innerHTML = `
    <div class="rank">#${safe(c.rank)}</div>
    <h3>${safe(c.name)}</h3>
    <p>${safe(c.role)}</p>

    <div class="scores">
      <span>M: ${safe(c.match_score)}</span>
      <span>E: ${safe(c.engagement_score)}</span>
      <span>F: ${safe(c.final_score)}</span>
    </div>

    <div class="skills">
      ${(c.top_skills || []).map(s => `<span>${s}</span>`).join("")}
    </div>
  `

  return el
}