export function updateMetrics(data) {
  document.querySelector("#totalCandidates").innerText = data.total_candidates
  document.querySelector("#shortlisted").innerText = data.shortlist_count
  document.querySelector("#latency").innerText = data.latency + "s"
}