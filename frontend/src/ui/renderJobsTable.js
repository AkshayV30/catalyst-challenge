const sampleJDs = [
  {
    title: "Data Scientist",
    jd: "Analyze large datasets, build ML models, interpret data patterns..."
  },
  {
    title: "Backend Engineer",
    jd: "Build scalable APIs, microservices, database systems..."
  },
  {
    title: "DevOps Engineer",
    jd: "CI/CD pipelines, Kubernetes, cloud infrastructure automation..."
  }
]

export function renderJobsTable() {
  const container = document.querySelector("#jobsTable")

  container.innerHTML = `
    <h2>Sample Job Descriptions</h2>
    <table>
      <thead>
        <tr>
          <th>Role</th>
          <th>Description</th>
          <th>Use</th>
        </tr>
      </thead>
      <tbody>
        ${sampleJDs.map(j => `
          <tr>
            <td>${j.title}</td>
            <td>${j.jd}</td>
            <td><button onclick="document.querySelector('#jdInput').value='${j.jd}'">Use</button></td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `
}