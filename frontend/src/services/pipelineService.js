import { scoutAPI } from "../api/scout.api.js"
import { store } from "../store/appStore.js"

export async function runPipeline(jd, mode) {
  store.loading = true
  store.jd = jd
  store.mode = mode

  try {
    const data = await scoutAPI.run({ jd, mode })
    store.result = data
    return data
  } finally {
    store.loading = false
  }
}