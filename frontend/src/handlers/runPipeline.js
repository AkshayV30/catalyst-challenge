import { runScout } from "../api/scoutAPI.js"
import { renderResults } from "../ui/renderResults.js"
import { updateMetrics } from "../ui/renderMetrics.js"

export function attachHandlers() {
  const runBtn = document.querySelector("#runBtn")

  runBtn.onclick = async () => {
    const jd = document.querySelector("#jdInput").value
    const mode = document.querySelector("#mode").value
    const statusBox = document.querySelector("#statusBox")

    if (!jd) {
      alert("Please enter JD")
      return
    }

    statusBox.innerText = "Running pipeline..."

    try {
      const data = await runScout({ jd, mode })

      statusBox.innerText = "Completed"

      updateMetrics(data)
      renderResults(data.shortlist)

    } catch (err) {
      console.error(err)
      statusBox.innerText = "Error"
    }
  }
}