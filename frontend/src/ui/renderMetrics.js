export function renderMetrics(data) {
  document.querySelector("#total").innerText = data.total_candidates
  document.querySelector("#short").innerText = data.shortlist_count
  document.querySelector("#latency").innerText = `${data.latency}s`
}