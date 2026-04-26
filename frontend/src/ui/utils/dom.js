export const $ = (sel) => document.querySelector(sel)

export const setHTML = (el, html) => {
  if (el) el.innerHTML = html
}

export const create = (tag, className = "") => {
  const el = document.createElement(tag)
  if (className) el.className = className
  return el
}