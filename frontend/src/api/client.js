const BASE_URL = "http://localhost:8008"

async function request(endpoint, payload) {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    throw new Error(await res.text())
  }

  return res.json()
}

export { BASE_URL, request }