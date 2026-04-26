import { $ } from "../utils/dom"
import { safe } from "../utils/format"

export function renderMetrics(data = {}) {
  $("#total").innerText = safe(data.total_candidates)
  $("#short").innerText = safe(data.shortlist_count)
  $("#latency").innerText = `${safe(data.latency)}s`
}