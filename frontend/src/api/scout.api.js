import { request } from "./client.js"

export const scoutAPI = {
  run: (payload) => request("/scout", payload),
}