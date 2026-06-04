import Constants from "expo-constants";
import { Platform } from "react-native";

const extra = Constants.expoConfig?.extra || {};
const extraFirebaseConfig = extra.firebase || {};

function valueFromEnv(name, extraValue) {
  const value = process.env[name] || extraValue || "";
  return typeof value === "string" ? value.trim() : value;
}

export const buildInfo = {
  appName: Constants.expoConfig?.name || "SiteSpy",
  appVersion: Constants.expoConfig?.version || "unknown",
  appEnvironment: extra.appEnvironment || process.env.APP_ENV || "development",
  buildProfile: extra.buildProfile || process.env.EAS_BUILD_PROFILE || "",
  platform: Platform.OS,
  hasExpoExtra: Boolean(Constants.expoConfig?.extra),
  hasFirebaseExtra: Boolean(extra.firebase)
};

export const firebaseConfig = {
  apiKey: valueFromEnv("EXPO_PUBLIC_FIREBASE_API_KEY", extraFirebaseConfig.apiKey),
  authDomain: valueFromEnv("EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN", extraFirebaseConfig.authDomain),
  projectId: valueFromEnv("EXPO_PUBLIC_FIREBASE_PROJECT_ID", extraFirebaseConfig.projectId),
  storageBucket: valueFromEnv("EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET", extraFirebaseConfig.storageBucket),
  messagingSenderId: valueFromEnv("EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID", extraFirebaseConfig.messagingSenderId),
  appId: valueFromEnv("EXPO_PUBLIC_FIREBASE_APP_ID", extraFirebaseConfig.appId),
  measurementId: valueFromEnv("EXPO_PUBLIC_FIREBASE_MEASUREMENT_ID", extraFirebaseConfig.measurementId)
};

export const missingFirebaseConfigKeys = Object.entries(firebaseConfig)
  .filter(([key, value]) => key !== "measurementId" && !value)
  .map(([key]) => key);

export const firebaseConfigFlags = Object.fromEntries(
  Object.entries(firebaseConfig).map(([key, value]) => [key, Boolean(value)])
);

export const isFirebaseConfigured = missingFirebaseConfigKeys.length === 0;

export const shouldShowRuntimeConfigDiagnostic =
  !isFirebaseConfigured && buildInfo.appEnvironment !== "production";

export function logStartupDiagnostics() {
  console.log("[SiteSpy] Startup", {
    version: buildInfo.appVersion,
    platform: buildInfo.platform,
    appEnvironment: buildInfo.appEnvironment,
    buildProfile: buildInfo.buildProfile,
    hasExpoExtra: buildInfo.hasExpoExtra,
    hasFirebaseExtra: buildInfo.hasFirebaseExtra
  });
  console.log("[SiteSpy] Firebase config key presence", firebaseConfigFlags);
  if (!isFirebaseConfigured) {
    console.warn("[SiteSpy] Missing Firebase config keys:", missingFirebaseConfigKeys);
  }
}
