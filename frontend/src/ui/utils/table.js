export function renderTable({ columns, rows }) {
  return `
    <table>
      <thead>
        <tr>
          ${columns.map(c => `<th>${c.label}</th>`).join("")}
        </tr>
      </thead>
      <tbody>
        ${rows.map(row => `
          <tr>
            ${columns.map(c => `<td>${c.render(row)}</td>`).join("")}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `
}