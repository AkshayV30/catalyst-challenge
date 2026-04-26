export function renderApp() {
  document.querySelector("#app").innerHTML = `
    <div class="app">

      <header class="header">
        <h1>AI Recruiter Dashboard</h1>
        <p>JD → Matching → Engagement → Ranking</p>
      </header>

      <section class="panel">
        <textarea id="jdInput" placeholder="Paste JD..."></textarea>

        <div class="controls">
          <select id="mode">
            <option value="default">Default</option>
            <option value="balanced">Balanced</option>
            <option value="strict">Strict</option>
          </select>

          <button id="runBtn">Run Pipeline</button>
        </div>
      </section>

      <div id="statusBox">Idle</div>

      <section class="metrics">
        <div class="card">Total: <span id="total">-</span></div>
        <div class="card">Shortlisted: <span id="short">-</span></div>
        <div class="card">Latency: <span id="latency">-</span></div>
      </section>

      <section id="results"></section>

    </div>
  `
}