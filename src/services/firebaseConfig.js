import { getApp, getApps, initializeApp } from "firebase/app";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Platform } from "react-native";
import * as FirebaseAuth from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";
import { firebaseConfig, isFirebaseConfigured, missingFirebaseConfigKeys } from "./runtimeConfig";

function getAsyncStoragePersistence(storage) {
  return class ReactNativeAsyncStoragePersistence {
    static type = "LOCAL";

    constructor() {
      this.type = "LOCAL";
    }

    async _isAvailable() {
      try {
        const testKey = "sitespy.firebase.auth.persistence";
        await storage.setItem(testKey, "1");
        await storage.removeItem(testKey);
        return true;
      } catch {
        return false;
      }
    }

    _set(key, value) {
      return storage.setItem(key, JSON.stringify(value));
    }

    async _get(key) {
      const value = await storage.getItem(key);
      return value ? JSON.parse(value) : null;
    }

    _remove(key) {
      return storage.removeItem(key);
    }

    _addListener() {}

    _removeListener() {}
  };
}

let firebaseApp = null;
let auth = null;
let db = null;
let storage = null;

if (isFirebaseConfigured) {
  try {
    firebaseApp = getApps().length ? getApp() : initializeApp(firebaseConfig);
    if (Platform.OS !== "web") {
      try {
        auth = FirebaseAuth.initializeAuth(firebaseApp, {
          persistence: getAsyncStoragePersistence(AsyncStorage)
        });
      } catch (authError) {
        if (authError?.code === "auth/already-initialized") {
          auth = FirebaseAuth.getAuth(firebaseApp);
        } else {
          throw authError;
        }
      }
    } else {
      auth = FirebaseAuth.getAuth(firebaseApp);
    }
    db = getFirestore(firebaseApp);
    storage = getStorage(firebaseApp);
  } catch (error) {
    console.error("[SiteSpy] Firebase initialization failed", error);
  }
} else {
  console.warn("[SiteSpy] Missing Firebase config keys:", missingFirebaseConfigKeys);
}

export { firebaseApp, auth, db, storage };

export function requireFirebase() {
  if (!isFirebaseConfigured || !auth || !db || !storage) {
    const error = new Error("Firebase environment values are missing. Create .env from .env.example and restart Expo.");
    error.code = "firebase/missing-config";
    throw error;
  }
}
