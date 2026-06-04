import { DEFAULT_WASTE_FACTOR } from "./constants";

function round(value) {
  return Math.round(Number(value || 0) * 100) / 100;
}

export function calculateWallEstimate(input) {
  const wallLength = Number(input.wallLength);
  const wallHeight = Number(input.wallHeight);
  const unitLength = Number(input.unitLength);
  const unitHeight = Number(input.unitHeight);
  const unitPrice = Number(input.unitPrice);
  const labourRate = Number(input.labourRate);
  const mortarPrice = Number(input.mortarPrice ?? input.mortarRate ?? 0);
  const mortarAllowance = Number(input.mortarAllowance || 0.03);
  const wasteFactor = Number(input.wasteFactor || DEFAULT_WASTE_FACTOR);

  // Simple undergraduate estimate: area of wall divided by face area of one masonry unit.
  const wallArea = wallLength * wallHeight;
  const unitArea = unitLength * unitHeight;
  const estimatedUnits = Math.ceil((wallArea / unitArea) * wasteFactor);

  // Mortar quantity is treated as a small volume allowance over the wall face area.
  const wallThickness = Number(input.wallThickness || 0);
  const mortarQuantity = round(wallArea * Math.max(wallThickness, mortarAllowance) * mortarAllowance);

  const materialCost = round(estimatedUnits * unitPrice);
  const mortarCost = round(mortarQuantity * mortarPrice);
  const labourCost = round(wallArea * labourRate);
  const totalCost = round(materialCost + mortarCost + labourCost);

  return {
    wallLength: round(wallLength),
    wallHeight: round(wallHeight),
    wallThickness: round(wallThickness),
    wallArea: round(wallArea),
    unitType: input.unitType,
    unitLength: round(unitLength),
    unitHeight: round(unitHeight),
    estimatedUnits,
    mortarQuantity,
    unitPrice: round(unitPrice),
    mortarPrice: round(mortarPrice),
    labourRate: round(labourRate),
    wasteFactor: round(wasteFactor),
    materialCost,
    mortarCost,
    labourCost,
    totalCost,
    boqSummary: [
      { item: "Masonry units", quantity: estimatedUnits, unit: input.unitType, rate: round(unitPrice), amount: materialCost },
      { item: "Mortar allowance", quantity: mortarQuantity, unit: "m3", rate: round(mortarPrice), amount: mortarCost },
      { item: "Labour", quantity: round(wallArea), unit: "m2", rate: round(labourRate), amount: labourCost }
    ]
  };
}
