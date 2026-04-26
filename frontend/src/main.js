import "./style.css"

import { renderApp } from "./ui/renderApp.js"
import {  initTabs } from "./ui/tabs.js"
import { runPipeline } from "./services/pipelineService.js"

import { showLoading, showDone, showError, initLoader } from "./ui/loader"
import { renderJobsTable } from "./ui/renderJobsTable"
import { renderCandidatesTable } from "./ui/renderCandidatesTable"
import { renderResultsTable } from "./ui/renderResultsTable"

// ---------------- INIT ----------------
renderApp()

initTabs()
initLoader()

// DOM refs AFTER render
const jdInput = document.querySelector("#jdInput")
const modeSelect = document.querySelector("#mode")
const runBtn = document.querySelector("#runBtn")

// ---------------- LOAD DATA ----------------
renderJobsTable()
renderCandidatesTable()

// ---------------- RUN PIPELINE ----------------
runBtn.onclick = async () => {
  const jd = jdInput.value
  const mode = modeSelect.value

  if (!jd) return alert("Enter Job Description")

  try {
    showLoading("Processing JD")

    const data = await runPipeline(jd, mode)

    showDone()
    renderResultsTable(data.shortlist, data)

  } catch (err) {
    console.error(err)
    showError("Pipeline failed")
  }
}