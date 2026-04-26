export function setStatus(text) {
  document.querySelector("#statusBox").innerText = text
}

export function showLoading() {
  setStatus("Running AI Pipeline...")
}

export function showDone() {
  setStatus("Completed")
}

export function showError() {
  setStatus("Error")
}