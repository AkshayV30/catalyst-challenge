import "./style.css"

import { renderApp } from "./ui/renderApp.js"
import { runPipeline } from "./services/pipelineService.js"

import { showLoading, showDone, showError } from "./ui/loader"
import { renderMetrics } from "./ui/renderMetrics"
import { renderResults } from "./ui/renderResults"

renderApp()

const jdInput = document.querySelector("#jdInput")
const modeSelect = document.querySelector("#mode")
const runBtn = document.querySelector("#runBtn")

runBtn.onclick = async () => {
  const jd = jdInput.value
  const mode = modeSelect.value

  if (!jd) return alert("Enter JD")

  try {
    showLoading()

    const data = await runPipeline(jd, mode)

    showDone()

    renderMetrics(data)
    renderResults(data.shortlist)

  } catch (err) {
    console.error(err)
    showError()
  }
}