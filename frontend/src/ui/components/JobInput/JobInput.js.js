import { renderModeOptions } from "../../renderers/modeOptions.js"

export function JobInput() {
  return `
    <section class="panel job-input">

      <textarea id="jdInput" placeholder="Paste Job Description..."></textarea>

      <div class="controls">
        <div class="control-group">
          <label>Matching Mode</label>
          <select id="mode">
            ${renderModeOptions()}
          </select>
        </div>

        <button id="runBtn" class="primary-btn">
          Run Pipeline
        </button>
      </div>

      <div class="mode-desc" id="modeDesc"></div>

      <div class="status-wrapper">
        <div class="status-label">Pipeline Status</div>
        <div id="statusBox">Idle</div>
      </div>

    </section>
  `
}