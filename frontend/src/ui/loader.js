let statusEl = null
let intervalId = null

// -------------------- INIT --------------------
export function initLoader(selector = "#statusBox") {
  statusEl = document.querySelector(selector)
}

// -------------------- CORE UTILS --------------------
function setStatus(text) {
  if (!statusEl) return
  statusEl.innerText = text
}

function clearLoader() {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

// -------------------- LOADING ANIMATION --------------------
function startDots(stage) {
  clearLoader()

  let dots = 0

  intervalId = setInterval(() => {
    dots = (dots + 1) % 4
    setStatus(`${stage}${".".repeat(dots)}`)
  }, 400)
}

// -------------------- PUBLIC API --------------------
export function showLoading(stage = "Initializing") {
  startDots(stage)
}

export function updateStage(stage, meta) {
  clearLoader()

  if (meta === undefined || meta === null) {
    setStatus(stage)
    return
  }

  setStatus(`${stage} | ${typeof meta === "object" ? JSON.stringify(meta) : meta}`)
}

export function showDone(message = "Completed successfully") {
  clearLoader()
  setStatus(message)
}

export function showError(message = "Error") {
  clearLoader()
  setStatus(` ${message}`)
}