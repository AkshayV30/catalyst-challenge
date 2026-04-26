let statusEl = null
let intervalId = null

// ---------------- INIT ----------------
export function initLoader(selector = "#statusBox") {
  statusEl = document.querySelector(selector)
}

// ---------------- CORE ----------------
function setStatus(html) {
  if (!statusEl) return
  statusEl.innerHTML = html
}

function clearLoader() {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

// ---------------- DOT ANIMATION ----------------
function startDots(stage) {
  clearLoader()

  let dots = 0

  intervalId = setInterval(() => {
    dots = (dots + 1) % 4
    setStatus(`
      <div class="status-stage">
        <span class="pulse">●</span> ${stage}
        <span class="dots">${".".repeat(dots)}</span>
      </div>
    `)
  }, 400)
}

// ---------------- PUBLIC API ----------------
export function showLoading(stage = "Initializing pipeline") {
  startDots(stage)
}

export function updateStage(stage, meta) {
  clearLoader()

  const metaText =
    meta === undefined || meta === null
      ? ""
      : typeof meta === "object"
      ? JSON.stringify(meta, null, 2)
      : String(meta)

  setStatus(`
    <div class="status-block">
      <div class="status-title">${stage}</div>
      ${metaText ? `<div class="status-meta">${metaText}</div>` : ""}
    </div>
  `)
}

export function showDone(message = "Pipeline completed") {
  clearLoader()

  setStatus(`
    <div class="status-success">
       ${message}
    </div>
  `)
}

export function showError(message = "Pipeline failed") {
  clearLoader()

  setStatus(`
    <div class="status-error">
       ${message}
    </div>
  `)
}