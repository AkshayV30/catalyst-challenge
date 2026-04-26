export async function runScouting({ jd, mode }) {
  const res = await fetch("http://localhost:8000/scout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jd, mode })
  })

  if (!res.ok) throw new Error("API failed")

  return await res.json()
}