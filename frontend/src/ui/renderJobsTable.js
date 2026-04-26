import { getJobs } from "../api/data.api.js"

export async function renderJobsTable() {
  const container = document.querySelector("#jobsTable")

  container.innerHTML = `<p>Loading jobs...</p>`

  try {
    const data = await getJobs()
    const jobs = data?.jobs || []

    if (!jobs.length) {
      container.innerHTML = `<p>No jobs found</p>`
      return
    }

    container.innerHTML = `
      <h2>Sample Job Descriptions</h2>
      <table border="1" cellpadding="8" cellspacing="0">
        <thead>
          <tr>
            <th>Role</th>
            <th>Description</th>
            <th>Responsibilities</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody id="jobsBody"></tbody>
      </table>
    `

    const tbody = document.querySelector("#jobsBody")

    jobs.forEach((job) => {
      const row = document.createElement("tr")

      const responsibilities = (job.key_responsibilities || [])
        .slice(0, 3)
        .join(" • ")

      row.innerHTML = `
        <td>${job.role ?? "-"}</td>
        <td>${job.job_description ?? "-"}</td>
        <td>${responsibilities || "-"}</td>
        <td><button class="use-btn">Use</button></td>
      `

      const btn = row.querySelector(".use-btn")

      btn.addEventListener("click", () => {
        const input = document.querySelector("#jdInput")

        if (input) {
          input.value = job.job_description
        }
      })

      tbody.appendChild(row)
    })
  } catch (err) {
    console.error(err)
    container.innerHTML = `<p>Failed to load jobs</p>`
  }
}