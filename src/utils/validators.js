export function requireText(value, label) {
  if (!String(value || "").trim()) {
    return `${label} is required.`;
  }
  return "";
}

export function requirePositiveNumber(value, label) {
  const number = Number(value);
  if (!Number.isFinite(number) || number <= 0) {
    return `${label} must be greater than zero.`;
  }
  return "";
}

export function validateEmail(value) {
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value || ""))) {
    return "Enter a valid email address.";
  }
  return "";
}

export function collectErrors(checks) {
  return checks.map((check) => check()).filter(Boolean);
}
