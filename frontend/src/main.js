import "./style.css"
import { renderApp } from "./ui/renderApp.js"
import { attachHandlers } from "./handlers/runPipeline.js"

renderApp()

attachHandlers()