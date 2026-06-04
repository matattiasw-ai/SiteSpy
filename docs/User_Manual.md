# SiteSpy User Manual

## Installation

Install Expo Go on an Android phone, run `npm install`, then start the app with `npm start`. Scan the QR code from the Expo terminal.

For APK testing, build with `npm run build:apk` after EAS login and install the generated APK on Android.

## Login and Registration

Open the app and choose **Create account** to register with an email and password. Existing users can log in from the login screen. Use **Forgot password** to request a Firebase password reset email. Users can also request **Email me a sign-in link** for passwordless Firebase email link sign-in.

Google sign-in is currently disabled in the app UI while OAuth client IDs and redirect setup are finalized.

## Creating a Project

Go to the **New** tab, enter a project title, add optional notes, and tap **Create and estimate**. The app opens the manual estimate screen for that project.

## Manual Estimation

Enter wall length, wall height, unit dimensions, unit price, labour rate, and mortar price. Choose brick or concrete block to load default unit sizes. The preview card shows wall area, estimated units, mortar quantity, and total cost. Tap **Save estimate** to store the result in Firestore.

## Image-Assisted Estimation

From a project or the manual estimate screen, open **Image-assisted estimate**. Choose a gallery image or capture a camera photo, then enter a real reference measurement in metres. The app first tries to upload the wall image to Firebase Storage and records the download URL in Firestore.

If Storage is unavailable, the app compresses the image and saves a small image data record in Firestore. If the compressed image is too large, choose a smaller or clearer image.

SiteSpy does not claim automatic AI wall detection. Image assistance depends on the user-entered reference measurement.

## Viewing History

Open the **Projects** tab to view saved projects. Tap a project to see details, estimates, images, and project actions.

## Editing and Deleting

From project details, tap **Edit project** to update the title, description, or location. Tap **Delete project** to remove the project document.

## Profile and Settings

Open the **Profile** tab to view account email and user id. Settings includes draft preference toggles and Android target information. Use **Log out** to end the Firebase session.

## Common Errors

- Missing Firebase values: copy `.env.example` to `.env`, fill all Firebase values, and restart Expo.
- Permission denied: confirm Firestore and Storage rules are deployed and the user is signed in.
- Image permission denied: allow camera or gallery access in Android settings.
- Build fails: run `npm run check`, `npm run doctor`, and confirm Expo/EAS login.
