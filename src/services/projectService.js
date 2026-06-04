import {
  addDoc,
  collection,
  deleteDoc,
  doc,
  getDoc,
  getDocs,
  query,
  serverTimestamp,
  updateDoc,
  where
} from "firebase/firestore";
import { COLLECTIONS } from "../utils/constants";
import { db, requireFirebase } from "./firebaseConfig";

function withId(snapshot) {
  return { id: snapshot.id, ...snapshot.data() };
}

function sortByCreatedAtDesc(items) {
  return items.sort((a, b) => {
    const left = a.createdAt?.toMillis ? a.createdAt.toMillis() : 0;
    const right = b.createdAt?.toMillis ? b.createdAt.toMillis() : 0;
    return right - left;
  });
}

export async function createProject(userId, data) {
  requireFirebase();
  const payload = {
    userId,
    title: data.title.trim(),
    description: data.description?.trim() || "",
    location: data.location?.trim() || "",
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp()
  };
  const reference = await addDoc(collection(db, COLLECTIONS.projects), payload);
  await updateDoc(reference, { projectId: reference.id });
  return { id: reference.id, projectId: reference.id, ...payload };
}

export async function listProjects(userId) {
  requireFirebase();
  const projectQuery = query(collection(db, COLLECTIONS.projects), where("userId", "==", userId));
  const snapshot = await getDocs(projectQuery);
  return sortByCreatedAtDesc(snapshot.docs.map(withId));
}

export async function getProject(projectId) {
  requireFirebase();
  const snapshot = await getDoc(doc(db, COLLECTIONS.projects, projectId));
  if (!snapshot.exists()) {
    throw new Error("Project was not found.");
  }
  return withId(snapshot);
}

export async function updateProject(projectId, data) {
  requireFirebase();
  await updateDoc(doc(db, COLLECTIONS.projects, projectId), {
    title: data.title.trim(),
    description: data.description?.trim() || "",
    location: data.location?.trim() || "",
    updatedAt: serverTimestamp()
  });
}

export async function deleteProject(projectId) {
  requireFirebase();
  await deleteDoc(doc(db, COLLECTIONS.projects, projectId));
}

export async function saveEstimation(userId, projectId, estimate) {
  requireFirebase();
  const payload = {
    projectId,
    userId,
    ...estimate,
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp()
  };
  const reference = await addDoc(collection(db, COLLECTIONS.estimations), payload);
  await updateDoc(reference, { estimationId: reference.id });
  await updateDoc(doc(db, COLLECTIONS.projects, projectId), { updatedAt: serverTimestamp() });
  return { id: reference.id, estimationId: reference.id, ...payload };
}

export async function listEstimations(userId, projectId) {
  requireFirebase();
  const estimationQuery = query(
    collection(db, COLLECTIONS.estimations),
    where("userId", "==", userId),
    where("projectId", "==", projectId)
  );
  const snapshot = await getDocs(estimationQuery);
  return sortByCreatedAtDesc(snapshot.docs.map(withId));
}

export async function saveWallImage(userId, projectId, imageData) {
  requireFirebase();
  const payload = {
    imageId: imageData.imageId,
    projectId,
    userId,
    storagePath: imageData.storagePath || "",
    downloadURL: imageData.downloadURL || imageData.imageUrl || "",
    imageUrl: imageData.downloadURL || imageData.imageUrl || "",
    localUri: imageData.localUri || "",
    status: imageData.status || "uploaded",
    fileName: imageData.fileName || "",
    mimeType: imageData.mimeType || "image/jpeg",
    size: imageData.size || null,
    referenceMeasurement: Number(imageData.referenceMeasurement),
    createdAt: serverTimestamp(),
    uploadedAt: serverTimestamp()
  };
  const reference = await addDoc(collection(db, COLLECTIONS.wallImages), payload);
  await updateDoc(reference, { imageId: reference.id });
  await updateDoc(doc(db, COLLECTIONS.projects, projectId), { updatedAt: serverTimestamp() });
  return { id: reference.id, imageId: reference.id, ...payload };
}

export async function listWallImages(userId, projectId) {
  requireFirebase();
  const imageQuery = query(
    collection(db, COLLECTIONS.wallImages),
    where("userId", "==", userId),
    where("projectId", "==", projectId)
  );
  const snapshot = await getDocs(imageQuery);
  return snapshot.docs.map(withId).sort((a, b) => {
    const left = a.uploadedAt?.toMillis ? a.uploadedAt.toMillis() : 0;
    const right = b.uploadedAt?.toMillis ? b.uploadedAt.toMillis() : 0;
    return right - left;
  });
}
