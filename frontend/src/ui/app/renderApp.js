import { Header } from "../components/Header.js"
import { Tabs } from "../components/Tabs/Tabs.js"

import { JobInput } from "../components/JobInput/JobInput.js"
import { JobsSection } from "../components/JobInput/JobsSection.js"
import { CandidatesSection } from "../components/Candidates/CandidatesSection.js"
import { PipelineSection } from "../components//PipeLine/PipelineSection.js"

export function renderApp() {
  document.querySelector("#app").innerHTML = `
    <div class="app">

      ${Header()}

      ${JobInput()}

      ${Tabs()}

      ${JobsSection()}

      ${CandidatesSection()}

      ${PipelineSection()}

    </div>
  `
}