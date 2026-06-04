import { getDownloadURL, ref, uploadBytesResumable } from "firebase/storage";
import { storage, requireFirebase } from "./firebaseConfig";

function extensionFromMimeType(mimeType = "image/jpeg") {
  if (mimeType.includes("png")) return "png";
  if (mimeType.includes("webp")) return "webp";
  return "jpg";
}

export async function uploadWallImage(userId, projectId, image) {
  requireFirebase();
  const imageUri = typeof image === "string" ? image : image?.uri;
  if (!imageUri) {
    const error = new Error("No image URI was provided.");
    error.code = "image/missing-uri";
    throw error;
  }

  const mimeType = image?.mimeType || "image/jpeg";
  const imageId = image?.imageId || `${Date.now()}`;
  const fileName = image?.fileName || `${imageId}.${extensionFromMimeType(mimeType)}`;
  const response = await fetch(imageUri);
  const blob = await response.blob();
  const storagePath = `users/${userId}/projects/${projectId}/images/${fileName}`;
  const imageRef = ref(storage, storagePath);

  await new Promise((resolve, reject) => {
    const task = uploadBytesResumable(imageRef, blob, { contentType: mimeType });
    task.on("state_changed", undefined, reject, resolve);
  });

  const downloadURL = await getDownloadURL(imageRef);
  return {
    imageId,
    downloadURL,
    imageUrl: downloadURL,
    storagePath,
    fileName,
    mimeType,
    size: image?.fileSize || blob.size || null
  };
}
