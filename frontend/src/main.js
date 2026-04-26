import "./style.css"

import { runScouting } from "./api/scoutAPI.js"
import { store } from "./state/store"

import { showLoading, showDone, showError } from "./ui/loader"
import { renderCandidates } from "./ui/cards"

document.querySelector("#app").innerHTML = `
<div class="app">

  <header class="header">
    <h1>AI Recruiter Dashboard</h1>
    <p>JD → Matching → Engagement → Ranking</p>
  </header>

  <section class="panel">
    <h2>Job Description</h2>

    <textarea id="jdInput"></textarea>

    <select id="mode">
      <option value="default">Default</option>
      <option value="balanced">Balanced</option>
      <option value="strict">Strict</option>
    </select>

    <button id="runBtn">Run Pipeline</button>
  </section>

  <section class="status" id="statusBox">Idle</section>

  <section class="metrics">
    <div>Total: <span id="total">-</span></div>
    <div>Shortlisted: <span id="short">-</span></div>
    <div>Latency: <span id="latency">-</span></div>
  </section>

  <section id="results"></section>

</div>
`

const jdInput = document.querySelector("#jdInput")
const runBtn = document.querySelector("#runBtn")
const statusBox = document.querySelector("#statusBox")

const total = document.querySelector("#total")
const short = document.querySelector("#short")
const latency = document.querySelector("#latency")

const results = document.querySelector("#results")

runBtn.onclick = async () => {
  const jd = jdInput.value
  const mode = document.querySelector("#mode").value

  if (!jd) return alert("Enter JD")

  try {
    showLoading(statusBox)

    const data = await runScouting({ jd, mode })

    showDone(statusBox)

    total.innerText = data.total_candidates
    short.innerText = data.shortlist_count
    latency.innerText = data.latency + "s"

    renderCandidates(data.shortlist, results)

  } catch (err) {
    console.error(err)
    showError(statusBox)
  }
}