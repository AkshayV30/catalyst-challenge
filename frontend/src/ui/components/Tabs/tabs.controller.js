export function initTabs() {
  const buttons = document.querySelectorAll(".tab-btn")
  const tabs = document.querySelectorAll(".tab-content")

  buttons.forEach(btn => {
    btn.onclick = () => {
      const target = btn.dataset.tab

      buttons.forEach(b => b.classList.remove("active"))
      tabs.forEach(t => t.classList.remove("active"))

      btn.classList.add("active")
      document.getElementById(target)?.classList.add("active")
    }
  })
}