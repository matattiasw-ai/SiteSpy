import {
  createUserWithEmailAndPassword,
  isSignInWithEmailLink,
  onAuthStateChanged,
  sendSignInLinkToEmail,
  sendPasswordResetEmail,
  signInWithEmailLink,
  signInWithEmailAndPassword,
  signOut
} from "firebase/auth";
import { doc, serverTimestamp, setDoc } from "firebase/firestore";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Platform } from "react-native";
import { COLLECTIONS, PASSWORDLESS_SIGN_IN_URL } from "../utils/constants";
import { clearSensitiveLocalState } from "./localStateService";
import { auth, db, requireFirebase } from "./firebaseConfig";

const PENDING_EMAIL_KEY = "sitespy.pendingEmailForSignIn";

async function storePendingEmail(email) {
  const trimmed = email.trim();
  if (Platform.OS === "web" && typeof window !== "undefined") {
    window.localStorage.setItem(PENDING_EMAIL_KEY, trimmed);
    return;
  }
  await AsyncStorage.setItem(PENDING_EMAIL_KEY, trimmed);
}

async function getPendingEmail() {
  if (Platform.OS === "web" && typeof window !== "undefined") {
    return window.localStorage.getItem(PENDING_EMAIL_KEY);
  }
  return AsyncStorage.getItem(PENDING_EMAIL_KEY);
}

async function clearPendingEmail() {
  if (Platform.OS === "web" && typeof window !== "undefined") {
    window.localStorage.removeItem(PENDING_EMAIL_KEY);
    return;
  }
  await AsyncStorage.removeItem(PENDING_EMAIL_KEY);
}

async function upsertUserProfile(user, profileData = {}) {
  await setDoc(doc(db, COLLECTIONS.users, user.uid), {
    userId: user.uid,
    email: user.email || "",
    displayName: profileData.displayName || user.displayName || "",
    photoURL: user.photoURL || "",
    updatedAt: serverTimestamp(),
    ...(profileData.createdAt ? { createdAt: profileData.createdAt } : {})
  }, { merge: true });
}

export function subscribeToAuthState(callback) {
  if (!auth) {
    console.warn("[SiteSpy] Firebase Auth is not configured; showing signed-out UI.");
    callback(null);
    return () => {};
  }
  return onAuthStateChanged(
    auth,
    callback,
    (error) => {
      console.error("[SiteSpy] Firebase auth state listener error", error);
      callback(null);
    }
  );
}

export async function registerWithEmail(email, password, profileData = {}) {
  requireFirebase();
  const credential = await createUserWithEmailAndPassword(auth, email.trim(), password);
  await upsertUserProfile(credential.user, { ...profileData, createdAt: serverTimestamp() });
  return credential.user;
}

export async function loginWithEmail(email, password) {
  requireFirebase();
  const credential = await signInWithEmailAndPassword(auth, email.trim(), password);
  return credential.user;
}

export async function sendPasswordReset(email) {
  requireFirebase();
  await sendPasswordResetEmail(auth, email.trim());
}

export async function sendPasswordlessSignInLink(email) {
  requireFirebase();
  const actionCodeSettings = {
    url: PASSWORDLESS_SIGN_IN_URL,
    handleCodeInApp: true
  };
  await sendSignInLinkToEmail(auth, email.trim(), actionCodeSettings);
  await storePendingEmail(email);
}

export async function completePasswordlessSignIn(email, url) {
  requireFirebase();
  const link = url || (typeof window !== "undefined" && window.location?.href ? window.location.href : "");
  if (!isSignInWithEmailLink(auth, link)) {
    return null;
  }
  const storedEmail = email?.trim() || await getPendingEmail();
  if (!storedEmail) {
    throw new Error("Enter your email again to complete passwordless sign-in.");
  }
  const credential = await signInWithEmailLink(auth, storedEmail, link);
  await clearPendingEmail();
  await upsertUserProfile(credential.user);
  return credential.user;
}

export async function completePasswordlessFromCurrentUrl() {
  const currentUrl = typeof window !== "undefined" && window.location?.href ? window.location.href : "";
  if (!currentUrl || !auth) {
    console.log("[SiteSpy] Passwordless URL check skipped", { hasUrl: Boolean(currentUrl), hasAuth: Boolean(auth) });
    return null;
  }
  return completePasswordlessSignIn("", currentUrl);
}

export async function logout() {
  requireFirebase();
  const userId = auth.currentUser?.uid;
  await signOut(auth);
  if (userId) {
    await clearSensitiveLocalState(userId);
  }
}

export const register = registerWithEmail;
export const login = loginWithEmail;
export const sendReset = sendPasswordReset;
