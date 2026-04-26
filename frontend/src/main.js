import "./style.css"

import { renderApp } from "./ui/app/renderApp.js"

import { initTabs } from "./ui/components/Tabs/tabs.controller.js"
import { initPipeline } from "./ui/components/PipeLine/pipeline.controller.js"
import { initJobInput } from "./ui/components/JobInput/jobinput.controller.js"

import { initLoader } from "./ui/utils/loader.js"

import { renderJobsTable } from "./ui/renderers/jobs.js"
import { renderCandidatesTable } from "./ui/renderers/candidates.js"

// render UI
renderApp()

// init behaviors
initTabs()
initLoader()
initPipeline()
initJobInput()

// load data
renderJobsTable()
renderCandidatesTable()