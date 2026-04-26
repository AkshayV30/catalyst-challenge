import { groupModes, DEFAULT_MODE } from "../utils/modes";

export function renderModeOptions() {
  return Object.entries(groupModes())
    .map(([group, items]) => `
      <optgroup label="${group}">
        ${items.map(m => `
          <option value="${m.key}" ${m.key === DEFAULT_MODE ? "selected" : ""}>
            ${m.label}
          </option>
        `).join("")}
      </optgroup>
    `).join("")
}