import { addDoc, collection, doc, serverTimestamp, updateDoc } from "firebase/firestore";
import { COLLECTIONS } from "../utils/constants";
import { db, requireFirebase } from "./firebaseConfig";

export async function saveWallImageData(userId, projectId, imageData = {}) {
  requireFirebase();
  const payload = {
    userId,
    projectId,
    width: imageData.width,
    height: imageData.height,
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
