import { formatCurrency, formatNumber } from "../utils/formatters";

export function createEstimateReport(project, estimate) {
  const title = project?.title || "Untitled project";
  const rows = estimate?.boqSummary || [
    { item: "Masonry units", quantity: estimate?.estimatedUnits || 0, unit: estimate?.unitType || "unit", rate: estimate?.unitPrice || 0, amount: estimate?.materialCost || 0 },
    { item: "Mortar allowance", quantity: estimate?.mortarQuantity || 0, unit: "m3", rate: estimate?.mortarPrice || 0, amount: estimate?.mortarCost || 0 },
    { item: "Labour", quantity: estimate?.wallArea || 0, unit: "m2", rate: estimate?.labourRate || 0, amount: estimate?.labourCost || 0 }
  ];

  return {
    title,
    projectId: project?.projectId || project?.id || "",
    totalCost: estimate?.totalCost || 0,
    summary: `${title}: ${formatNumber(estimate?.wallArea)} m2 wall, ${estimate?.estimatedUnits || 0} units, ${formatCurrency(estimate?.totalCost)} total.`,
    rows: rows.map((row) => ({
      ...row,
      quantityLabel: `${formatNumber(row.quantity, row.unit === "m3" ? 3 : 2)} ${row.unit}`,
      rateLabel: formatCurrency(row.rate),
      amountLabel: formatCurrency(row.amount)
    }))
  };
}
