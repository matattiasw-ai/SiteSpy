import AsyncStorage from "@react-native-async-storage/async-storage";

const KEY_PREFIX = "sitespy";

function keyFor(name, userId, suffix = "") {
  return `${KEY_PREFIX}:${name}:${userId}${suffix ? `:${suffix}` : ""}`;
}

async function readJson(key, fallback = null) {
  try {
    const value = await AsyncStorage.getItem(key);
    return value ? JSON.parse(value) : fallback;
  } catch (error) {
    console.warn("[SiteSpy] Local state read failed", { key, message: error?.message });
    return fallback;
  }
}

async function writeJson(key, value) {
  try {
    await AsyncStorage.setItem(key, JSON.stringify({ ...value, updatedAt: Date.now() }));
  } catch (error) {
    console.warn("[SiteSpy] Local state write failed", { key, message: error?.message });
  }
}

export async function setLastRoute(userId, route) {
  if (!userId || !route) return;
  await writeJson(keyFor("lastRoute", userId), route);
}

export async function getLastRoute(userId) {
  if (!userId) return null;
  return readJson(keyFor("lastRoute", userId));
}

export async function setActiveProject(userId, project) {
  if (!userId || !project?.projectId) return;
  await writeJson(keyFor("activeProject", userId), project);
}

export async function getActiveProject(userId) {
  if (!userId) return null;
  return readJson(keyFor("activeProject", userId));
}

export async function saveDraftEstimate(userId, projectId, values) {
  if (!userId || !projectId) return;
  await writeJson(keyFor("draftEstimate", userId, projectId), {
    projectId,
    values
  });
}

export async function getDraftEstimate(userId, projectId) {
  if (!userId || !projectId) return null;
  return readJson(keyFor("draftEstimate", userId, projectId));
}

export async function clearDraftEstimate(userId, projectId) {
  if (!userId || !projectId) return;
  await AsyncStorage.removeItem(keyFor("draftEstimate", userId, projectId));
}

export async function getPendingUploads(userId) {
  if (!userId) return [];
  return readJson(keyFor("pendingUploads", userId), []);
}

export async function savePendingUpload(userId, draft) {
  if (!userId || !draft?.imageId) return [];
  const current = await getPendingUploads(userId);
  const nextDraft = { ...draft, updatedAt: Date.now() };
  const next = [nextDraft, ...current.filter((item) => item.imageId !== draft.imageId)].slice(0, 10);
  await AsyncStorage.setItem(keyFor("pendingUploads", userId), JSON.stringify(next));
  return next;
}

export async function removePendingUpload(userId, imageId) {
  if (!userId || !imageId) return [];
  const current = await getPendingUploads(userId);
  const next = current.filter((item) => item.imageId !== imageId);
  await AsyncStorage.setItem(keyFor("pendingUploads", userId), JSON.stringify(next));
  return next;
}

export async function restoreLocalContext(userId) {
  if (!userId) {
    return { activeProject: null, lastRoute: null, pendingUploads: [] };
  }
  const [activeProject, lastRoute, pendingUploads] = await Promise.all([
    getActiveProject(userId),
    getLastRoute(userId),
    getPendingUploads(userId)
  ]);
  return { activeProject, lastRoute, pendingUploads };
}

export async function clearSensitiveLocalState(userId) {
  if (!userId) return;
  const keys = await AsyncStorage.getAllKeys();
  const userPrefix = `${KEY_PREFIX}:`;
  const matching = keys.filter((key) => key.startsWith(userPrefix) && key.includes(`:${userId}`));
  if (matching.length) {
    await AsyncStorage.multiRemove(matching);
  }
}
