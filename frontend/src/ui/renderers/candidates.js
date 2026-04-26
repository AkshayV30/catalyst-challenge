import { getCandidates } from "../../api/data.api"
import { $, setHTML } from "../utils/dom"
import { renderTable } from "../utils/table"
import { safe, listToString } from "../utils/format"

export async function renderCandidatesTable() {
  const container = $("#candidatesTable")
  setHTML(container, "Loading candidates...")

  try {
    const { candidates = [] } = await getCandidates()

    if (!candidates.length) {
      return setHTML(container, "No candidates found")
    }

    const columns = [
      { label: "Name", render: c => safe(c.name) },
      { label: "Role", render: c => safe(c.role) },
      { label: "Skills", render: c => listToString(c.skills) }
    ]

    setHTML(container, `
      <h2>Candidates</h2>
      ${renderTable({ columns, rows: candidates })}
    `)

  } catch (err) {
    console.error(err)
    setHTML(container, "Failed to load candidates")
  }
}