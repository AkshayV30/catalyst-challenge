import { $ } from "../../utils/dom.js"
import { runPipeline } from "../../../services/pipelineService.js"
import { showLoading, showDone, showError } from "../../utils/loader.js"
import { renderResultsTable } from "../../renderers/results.js"
import { renderMetrics } from "../../renderers/metrics.js"

export function initPipeline() {
  const runBtn = $("#runBtn")

  runBtn.onclick = async () => {
    const jd = $("#jdInput").value
    const mode = $("#mode").value

    if (!jd) return alert("Enter Job Description")

    try {
      showLoading("Processing JD")

      const data = await runPipeline(jd, mode)

      showDone()

      renderResultsTable(data.shortlist, data)
      renderMetrics(data)

    } catch (err) {
      console.error(err)
      showError("Pipeline failed")
    }
  }
}