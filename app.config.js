export default ({ config }) => ({
  ...config,
  updates: {
    enabled: false
  },
  extra: {
    ...config.extra,
    appEnvironment: process.env.APP_ENV || process.env.EAS_BUILD_PROFILE || process.env.NODE_ENV || "development",
    buildProfile: process.env.EAS_BUILD_PROFILE || "",
    firebase: {
      apiKey: process.env.EXPO_PUBLIC_FIREBASE_API_KEY || "",
      authDomain: process.env.EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN || "",
      projectId: process.env.EXPO_PUBLIC_FIREBASE_PROJECT_ID || "",
      storageBucket: process.env.EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET || "",
      messagingSenderId: process.env.EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || "",
      appId: process.env.EXPO_PUBLIC_FIREBASE_APP_ID || "",
      measurementId: process.env.EXPO_PUBLIC_FIREBASE_MEASUREMENT_ID || ""
    },
    eas: {
      projectId: "1778bd05-4609-433e-9ec7-789aa44f4eaf"
    }
  }
});
