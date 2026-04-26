import { $, setHTML } from "../utils/dom"
import { renderTable } from "../utils/table"
import { safe } from "../utils/format"

export function renderResultsTable(list = [], meta = {}) {
  const container = $("#results")

  const columns = [
    { label: "Rank", render: c => `#${safe(c.rank)}` },
    { label: "Name", render: c => safe(c.name) },
    { label: "Role", render: c => safe(c.role) },
    { label: "Match", render: c => safe(c.match_score) },
    { label: "Engagement", render: c => safe(c.engagement_score) },
    { label: "Final", render: c => safe(c.final_score) },
  ]

  const summary = `
    <div class="summary">
      Total: ${safe(meta.total_candidates)} |
      Shortlisted: ${safe(meta.shortlist_count, list.length)} |
      Latency: ${safe(meta.latency)}s
    </div>
  `

  setHTML(container, `
    <h2>Ranked Shortlist</h2>
    ${summary}
    ${renderTable({ columns, rows: list })}
  `)
}