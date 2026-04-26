import { MODES, DEFAULT_MODE } from "../../utils/modes.js"

export function initJobInput() {
  const modeSelect = document.querySelector("#mode")
  const modeDesc = document.querySelector("#modeDesc")

  if (!modeSelect || !modeDesc) return

  const update = () => {
    const m = MODES[modeSelect.value || DEFAULT_MODE]
    if (!m) return

    modeDesc.innerHTML = `
      <div><strong>${m.label}</strong></div>
      <div class="muted">${m.desc}</div>
    `
  }

  modeSelect.addEventListener("change", update)
  update()
}