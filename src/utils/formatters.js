export function formatCurrency(value) {
  const number = Number(value || 0);
  return `N$ ${number.toFixed(2)}`;
}

export function formatDate(value) {
  if (!value) return "Not recorded";
  const date = value.toDate ? value.toDate() : new Date(value);
  return date.toLocaleDateString();
}

export function formatNumber(value, decimals = 2) {
  return Number(value || 0).toFixed(decimals);
}
