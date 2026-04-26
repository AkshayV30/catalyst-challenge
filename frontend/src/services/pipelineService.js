import { scoutAPI } from "../api/scoutAPI.js"
import { store } from "../state/store.js"

export async function runPipeline(jd, mode) {
  store.loading = true
  store.jd = jd
  store.mode = mode

  const data = await scoutAPI.run({ jd, mode })

  store.result = data
  store.loading = false

  return data
}