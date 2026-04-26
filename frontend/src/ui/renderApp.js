
export function renderApp() {
  document.querySelector("#app").innerHTML = `
    <div class="app">

      <header class="header">
        <h1>AI Recruiter</h1>
        <p>Matching → Engagement → Ranking</p>
      </header>

      <!-- TABS -->
      <div class="tabs">
        <button class="tab-btn active" data-tab="jobs">Jobs</button>
        <button class="tab-btn" data-tab="candidates">Candidates</button>
        <button class="tab-btn" data-tab="pipeline">Pipeline</button>
      </div>

      <!-- JOBS -->
      <section id="jobs" class="tab-content active">
        <div class="panel">
          <div id="jobsTable"></div>
        </div>

        <div class="panel">
          <textarea id="jdInput" placeholder="Paste JD..."></textarea>

          <div class="controls">
            <select id="mode">
              <option value="balanced">Balanced</option>
              <option value="loose">Loose</option>
              <option value="strict">Strict</option>
            </select>

            <button id="runBtn">Run</button>
          </div>

          <div class="status-wrapper">
            <div class="status-label">Status</div>
            <div id="statusBox">Idle</div>
          </div>
        </div>
      </section>

      <!-- CANDIDATES -->
      <section id="candidates" class="tab-content">
        <div class="panel">
          <div id="candidatesTable"></div>
        </div>
      </section>

      <!-- PIPELINE -->
      <section id="pipeline" class="tab-content">
        <div class="panel metrics">
          <div class="card"><h3>Total</h3><div id="total">-</div></div>
          <div class="card"><h3>Short</h3><div id="short">-</div></div>
          <div class="card"><h3>Latency</h3><div id="latency">-</div></div>
        </div>

        <div class="panel">
          <div id="results"></div>
        </div>
      </section>

    </div>
  `
}