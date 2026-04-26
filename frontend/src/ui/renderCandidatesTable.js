import { getCandidates } from "../api/data.api.js"

export async function renderCandidatesTable() {
  const container = document.querySelector("#candidatesTable")

  container.innerHTML = `<p>Loading candidates...</p>`

  try {
    const data = await getCandidates()
    const candidates = data?.candidates || []

    if (!candidates.length) {
      container.innerHTML = `<p>No candidates found</p>`
      return
    }

    const table = document.createElement("table")

    table.innerHTML = `
      <thead>
        <tr>
          <th>Name</th>
          <th>Role</th>
          <th>Skills</th>
        </tr>
      </thead>
      <tbody></tbody>
    `

    const tbody = table.querySelector("tbody")

    candidates.forEach((c) => {
      const row = document.createElement("tr")

      const skills = (c.skills || []).join(", ")

      row.innerHTML = `
        <td>${c.name ?? "-"}</td>
        <td>${c.role ?? "-"}</td>
        <td>${skills}</td>
      `

      tbody.appendChild(row)
    })

    container.innerHTML = `
      <h2>Candidate Pool (Live Data)</h2>
    `

    container.appendChild(table)

  } catch (err) {
    console.error(err)
    container.innerHTML = `<p>Failed to load candidates</p>`
  }
}