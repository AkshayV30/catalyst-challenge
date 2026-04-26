import { getJobs } from "../../api/data.api"
import { $, setHTML, create } from "../utils/dom"
import { renderTable } from "../utils/table"
import { safe } from "../utils/format"

export async function renderJobsTable() {
  const container = $("#jobsTable")
  setHTML(container, "Loading jobs...")

  try {
    const { jobs = [] } = await getJobs()

    if (!jobs.length) {
      return setHTML(container, "No jobs found")
    }

    const columns = [
      { label: "Role", render: j => safe(j.role) },
      { label: "Description", render: j => safe(j.job_description) },
      {
        label: "Responsibilities",
        render: j => (j.key_responsibilities || []).slice(0, 3).join(" • ")
      },
      {
        label: "Action",
        render: () => `<button class="use-btn">Use</button>`
      }
    ]

    setHTML(container, `
      <h2>Jobs</h2>
      ${renderTable({ columns, rows: jobs })}
    `)

    // attach events (post-render)
    container.querySelectorAll(".use-btn").forEach((btn, i) => {
      btn.onclick = () => {
        $("#jdInput").value = jobs[i].job_description
      }
    })

  } catch (err) {
    console.error(err)
    setHTML(container, "Failed to load jobs")
  }
}