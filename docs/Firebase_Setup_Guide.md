# Firebase Setup Guide

## Required Services

Enable these Firebase services:

- Authentication with Email/Password.
- Email link/passwordless sign-in.
- Cloud Firestore.
- Firebase Storage if the project plan supports it.

## Environment Variables

Create `.env` from `.env.example` and fill the Firebase web app configuration:

```text
EXPO_PUBLIC_FIREBASE_API_KEY=
EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN=
EXPO_PUBLIC_FIREBASE_PROJECT_ID=
EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET=
EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
EXPO_PUBLIC_FIREBASE_APP_ID=
EXPO_PUBLIC_FIREBASE_MEASUREMENT_ID=
```

Never commit `.env` or service account credentials.

## Collections

- `users`: one document per Firebase user id.
- `projects`: user-owned project records.
- `estimations`: user-owned wall estimate records linked to a project.
- `wallImages`: user-owned compressed image records linked to a project.

Every app-owned record includes `userId`. Project and estimation records include timestamps.

## Rules

Deploy Firestore and Storage rules after selecting a Firebase project:

```bash
cp .firebaserc.example .firebaserc
firebase deploy --only firestore:rules,firestore:indexes,storage
```

Rules require authentication and restrict reads/writes to the matching `userId` or wall image storage path.

## Storage-First Image Workflow

SiteSpy now tries Firebase Storage first for wall images:

- The image is uploaded under `wallImages/{userId}/{fileName}`.
- Firestore stores `imageUrl`, `storagePath`, `projectId`, `userId`, and `referenceMeasurement`.
- Storage rules allow authenticated users to read and write only their own `wallImages/{userId}/` paths.

## Firestore Image Fallback

If Storage is unavailable, blocked, or not enabled, SiteSpy falls back to a safe Firestore image record:

- Selected wall images are resized to about 800 px width.
- Images are compressed as JPEG.
- The compressed base64 data URL is saved in `wallImages.imageDataUrl`.
- `byteEstimate`, `width`, and `height` are stored with the document.
- Oversized compressed images are rejected before upload so the app stays below the Firestore 1 MiB document limit.

Optional Storage fields are still supported:

- `imageUrl`
- `storagePath`

Keep Storage rules in the repo even when Storage is not used, so the project can use the same data model later.

## Authentication Providers

Firebase Auth providers must be enabled in the Firebase Console:

1. Open Firebase Console.
2. Go to **Authentication > Sign-in method**.
3. Enable **Email/Password**.
4. In the same provider settings, enable **Email link/passwordless sign-in**.
5. Check **Authentication > Settings > Authorized domains** and add any required Expo or hosting domains.
6. Keep `sitespy-alpha.web.app` authorized because passwordless links use `https://sitespy-alpha.web.app/auth/complete-signin`.

Google sign-in is currently disabled in the app UI. Re-enable it only after real Firebase/Google Cloud OAuth client IDs and redirect settings are finalized. Do not invent OAuth client IDs or commit them.

## Functions

`functions/` contains a health HTTPS function and a minimal callable report helper scaffold. It is not required for normal app operation; the mobile app calculates and saves estimates client-side.

## Optional Hosting

`hosting/` contains a small static support page. Hosting is optional and does not turn SiteSpy into a web app. The Android APK remains the primary deliverable.
