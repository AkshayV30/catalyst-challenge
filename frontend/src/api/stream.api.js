import { BASE_URL } from "./client.js"

export function streamScout(payload, onEvent) {
  const params = new URLSearchParams({
    jd: payload.jd,
    mode: payload.mode || "default",
  })

  const url = `${BASE_URL}/scout/stream?${params.toString()}`

  const es = new EventSource(url)

  es.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data)
      onEvent(data)
    } catch (err) {
      console.warn("Bad SSE chunk:", e.data)
    }
  }

  es.onerror = (err) => {
    console.error("SSE error:", err)
    es.close()
  }

  return es
}