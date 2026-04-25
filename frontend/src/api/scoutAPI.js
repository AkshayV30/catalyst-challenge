const BASE_URL = "http://localhost:8008"

export async function runScout(payload) {
  const res = await fetch(`${BASE_URL}/scout`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })

  if (!res.ok) {
    throw new Error("API request failed")
  }

  return res.json()
}