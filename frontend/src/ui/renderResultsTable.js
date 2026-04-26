export function renderResultsTable(list = [], meta = {}) {
  const container = document.querySelector("#results")

  container.innerHTML = `
    <h2>Ranked Shortlist</h2>

    <div class="summary">
      Total: ${meta.total_candidates ?? "-"} |
      Shortlisted: ${meta.shortlist_count ?? list.length} |
      Latency: ${meta.latency ?? "-"}s
    </div>

    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Name</th>
          <th>Role</th>
          <th>Match</th>
          <th>Engagement</th>
          <th>Final</th>
        </tr>
      </thead>

      <tbody>
        ${list.map(c => `
          <tr>
            <td>#${c.rank}</td>
            <td>${c.name}</td>
            <td>${c.role}</td>
            <td>${c.match_score}</td>
            <td>${c.engagement_score}</td>
            <td>${c.final_score}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `
}