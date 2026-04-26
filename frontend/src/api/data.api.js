import { request, BASE_URL } from "./client.js"


let jobsCache = null
let candidatesCache = null

export async function getJobs() {
  if (jobsCache) return jobsCache;

  const res = await fetch(`${BASE_URL}/jobs`)
  if (!res.ok) throw new Error(await res.text());

  jobsCache = await res.json()
  return jobsCache;
}

export async function getCandidates() {
  if (candidatesCache) return candidatesCache;

  const res = await fetch(`${BASE_URL}/candidates`);

  if (!res.ok) throw new Error(await res.text());

  candidatesCache = await res.json();
  return candidatesCache;
}