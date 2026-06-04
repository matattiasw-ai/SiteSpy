import { calculateWallEstimate } from "../utils/calculations";
import { saveEstimation } from "./projectService";

export function previewEstimate(input) {
  return calculateWallEstimate(input);
}

export async function calculateAndSaveEstimate(userId, projectId, input) {
  const estimate = calculateWallEstimate(input);
  return saveEstimation(userId, projectId, estimate);
}
