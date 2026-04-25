export function renderApp() {
  document.querySelector("#app").innerHTML = `
<div class="app">

  <header class="header">
    <h1>AI Recruiter Dashboard</h1>
    <p>JD → Matching → Engagement → Ranked Shortlist</p>
  </header>

  <section class="panel">
    <h2> Job Description</h2>

    <textarea id="jdInput" placeholder="Paste job description here..."></textarea>

    <div class="controls">
      <select id="mode">
        <option value="default">Default Mode</option>
        <option value="very_loose">Very Loose</option>
        <option value="strict">Strict</option>
      </select>

      <button id="runBtn">Run AI Pipeline</button>
    </div>
  </section>

  <section class="status">
    <div id="statusBox">Idle</div>
  </section>

  <section class="metrics">
    <div class="card">
      <h3>Total Candidates</h3>
      <div id="totalCandidates">-</div>
    </div>

    <div class="card">
      <h3>Shortlisted</h3>
      <div id="shortlisted">-</div>
    </div>

    <div class="card">
      <h3>Latency</h3>
      <div id="latency">-</div>
    </div>
  </section>

  <section class="results">
    <h2> Shortlisted Candidates</h2>
    <div id="resultsContainer"></div>
  </section>

</div>
`
}