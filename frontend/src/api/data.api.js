import { request, BASE_URL } from "./client.js"


export async function getCandidates() {
  const res = await fetch(`${BASE_URL}/candidates`)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function getJobs() {
  const res = await fetch(`${BASE_URL}/jobs`)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}