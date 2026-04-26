export function showLoading(statusBox) {
  statusBox.innerHTML = `
    <div class="loader"></div>
    Running AI Pipeline...
  `
}

export function showIdle(statusBox) {
  statusBox.innerText = "Idle"
}

export function showDone(statusBox) {
  statusBox.innerText = "Completed"
}

export function showError(statusBox) {
  statusBox.innerText = "Error"
}