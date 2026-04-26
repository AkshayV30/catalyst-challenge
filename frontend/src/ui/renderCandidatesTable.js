import { getCandidates } from "../api/data.api.js"

export async function renderCandidatesTable() {
  const container = document.querySelector("#candidatesTable")

  const data = await getCandidates()

  container.innerHTML = `
    <h2>Candidate Pool (Demo)</h2>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Role</th>
          <th>Skills</th>
        </tr>
      </thead>
      <tbody>
        ${data.candidates.map(c => `
          <tr>
            <td>${c.name}</td>
            <td>${c.role}</td>
            <td>${(c.skills || []).join(", ")}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `
}