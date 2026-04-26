 export const MODES = {
  very_loose: { label: "Very Loose", desc: "1+ skill • No required • 50/50 scoring", group: "Exploration" },
  loose: { label: "Loose", desc: "1+ skill • Relaxed filter • Slight match priority", group: "Exploration" },

  balanced: { label: "Balanced", desc: "2+ skills • 60% match / 40% engagement", group: "Balanced" },
  default: { label: "Default", desc: "2+ skills • 70% match • Stable shortlist", group: "Balanced" },

  focused: { label: "Focused", desc: "3+ skills • Required enforced", group: "Strict" },
  strict: { label: "Strict", desc: "3+ skills • Strong filtering • 85% match", group: "Strict" },
  very_strict: { label: "Very Strict", desc: "4+ skills • Hard filter • Max precision", group: "Strict" }
}

 export const DEFAULT_MODE = "balanced";

export function groupModes() {
  return Object.entries(MODES).reduce((acc, [key, m]) => {
    acc[m.group] ??= []
    acc[m.group].push({ key, ...m })
    return acc
  }, {})
}