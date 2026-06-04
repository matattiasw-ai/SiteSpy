import { doc, getDoc, serverTimestamp, setDoc, updateDoc } from "firebase/firestore";
import { COLLECTIONS } from "../utils/constants";
import { db, requireFirebase } from "./firebaseConfig";

export async function getUserProfile(userId) {
  requireFirebase();
  const snapshot = await getDoc(doc(db, COLLECTIONS.users, userId));
  if (!snapshot.exists()) {
    return null;
  }
  return { id: snapshot.id, ...snapshot.data() };
}

export async function createUserProfile(userId, data) {
  requireFirebase();
  const payload = {
    userId,
    email: data.email || "",
    displayName: data.displayName || "",
    phoneNumber: data.phoneNumber || "",
    discipline: data.discipline || "",
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp()
  };
  await setDoc(doc(db, COLLECTIONS.users, userId), payload, { merge: true });
  return payload;
}

export async function updateUserProfile(userId, data) {
  requireFirebase();
  const payload = {
    displayName: data.displayName || "",
    phoneNumber: data.phoneNumber || "",
    discipline: data.discipline || "",
    updatedAt: serverTimestamp()
  };
  await updateDoc(doc(db, COLLECTIONS.users, userId), payload);
  return payload;
}
