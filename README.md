# SiteSpy

SiteSpy is an Expo React Native Android app for masonry wall project estimation. It supports Firebase Authentication, Firestore-backed project history, compressed Firestore wall-image records, optional Firebase Storage support, and BOQ-style cost summaries for small construction projects.

## Stack

- Expo Managed Workflow
- React Native with JavaScript and JSX
- Firebase JS SDK
- Firebase Authentication, Firestore, and Storage
- React Navigation
- EAS Build for Android APK delivery

## Setup

```bash
npm install
cp .env.example .env
```

Fill `.env` with Firebase web app values:

```text
EXPO_PUBLIC_FIREBASE_API_KEY=
EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN=
EXPO_PUBLIC_FIREBASE_PROJECT_ID=
EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET=
EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
EXPO_PUBLIC_FIREBASE_APP_ID=
```

Do not commit `.env`, service account files, passwords, PATs, or raw collaborator files.

## Firebase Setup

1. Create a Firebase project and register a web app.
2. Enable Email/Password sign-in and Email link/passwordless sign-in.
3. Enable Cloud Firestore. Enable Firebase Storage only if the project plan supports it.
4. Copy `.firebaserc.example` to `.firebaserc` and replace the project id.
5. Deploy rules when ready:

```bash
firebase deploy --only firestore:rules,firestore:indexes,storage
```

Collections used by the app are `users`, `projects`, `estimations`, and `wallImages`. The default image workflow compresses selected wall photos and stores a small data URL in Firestore. Firebase Storage files are optional if the project plan supports Storage.

## Run With Expo Go

```bash
npm start
```

Scan the QR code with Expo Go on Android, or run:

```bash
npm run android
```

## Android APK Build

```bash
eas login
npm run build:apk
```

The `preview` EAS profile builds an APK. The `production` profile builds an Android App Bundle.

## Quality Checks

```bash
npm run check
npm run doctor
npm run export:android
```

The CI workflow runs `npm install` and `npm run check`. It does not require Android Studio and does not run EAS builds.

## Folder Structure

```text
src/
  navigation/      Auth stack, app tabs, and protected route shell
  screens/         Auth, dashboard, projects, estimates, profile, settings
  components/      Shared mobile UI components
  services/        Firebase Auth, Firestore, Storage, users, reports
  utils/           Calculations, validators, formatters, constants
  theme/           Colors, spacing, typography, shadows
firebase.json      Firebase deploy targets
firestore.rules    Authenticated owner-only Firestore rules
storage.rules      User-specific wall image storage rules
docs/              User, setup, testing, and submission documentation
project-management/ Student ownership and issue draft planning
```

## Implemented Features

- Splash, login, registration, forgot password, and protected app routing.
- Active Firebase Auth methods: email/password login, email/password registration, password reset, and passwordless email sign-in links.
- Dashboard with project and estimation metrics.
- Project create, read, update, delete, details, and history screens.
- Manual wall estimation for wall area, unit quantity, waste factor, mortar, material cost, labour, and total cost.
- Premium SiteSpy app assets applied for icon, splash, adaptive icon, favicon, and bundled logo assets.
- Image-assisted records using gallery/camera selection, compressed Firestore image data, optional Firebase Storage metadata, and user-entered reference measurement.
- BOQ-style estimate summary and report helper service.
- Profile and settings screens.
- Firebase rules, indexes, Functions scaffold, CI, and local project checks.

## Remaining Configuration

- Add real Firebase values to local `.env`.
- Enable Email/Password, Email link/passwordless sign-in, Firestore, and Storage in the Firebase Console.
- Google Auth is currently disabled in the app UI. It can be added later after OAuth client IDs and redirect setup are finalized.
- Deploy Firebase rules if the Firebase CLI project is configured.
- Test with Expo Go on Android.
- Run an EAS preview APK build before final submission.
- Students should validate assigned branches using their own GitHub accounts and Git identities.

## Contribution Workflow

1. Create the assigned branch from `main`.
2. Run `npm install` and `npm run check`.
3. Use your own Git identity for commits.
4. Do not commit secrets, `.env`, passwords, PATs, or raw collaborator files.
5. Open a pull request for review before merging.

## Showcase and Portfolio Requirements

- Group showcase slot: 20 minutes total, with 5 minutes intro, 5 minutes demo/comments, and 5 minutes panel questions/comments.
- Students should arrive at least 15 minutes early.
- Personal portfolio deadline: Sunday, 14 June 2026 at 23:59.
- Each personal portfolio must include a blog section with contribution reflection, evidence of work, learning summary, challenges, files owned/validation, and an individual contribution video or link.
- Individual contribution videos must be no longer than 1 minute 30 seconds.
