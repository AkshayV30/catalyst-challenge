export function renderApp() {
  document.querySelector("#app").innerHTML = `
    <div class="app">

      <header class="header">
        <h1>AI Recruiter Dashboard</h1>
        <p>JD → Matching → Engagement → Ranking</p>
      </header>

      <!-- 🔥 JOB LIBRARY -->
      <section id="jobsTable"></section>

      <!-- INPUT -->
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

      <!-- CANDIDATES -->
      <section id="candidatesTable"></section>

      <!-- RESULTS -->
      <section id="results"></section>

    </div>
  `
}