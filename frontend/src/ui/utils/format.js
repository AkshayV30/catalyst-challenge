export const safe = (v, fallback = "-") => v ?? fallback

export const listToString = (arr, sep = ", ") =>
  (arr || []).join(sep)