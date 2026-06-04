# Testing Checklist

## Local Checks

- Run `npm install`.
- Run `npm run check`.
- Run `npm run doctor`.
- Run `npm run export:android`.
- Confirm no `.env`, token, password, PAT, or raw collaborator files are staged.

## Auth Workflow

- Register with email and password.
- Log out and log in again.
- Request a password reset email.
- Confirm invalid email and short password errors display clearly.

## Project Workflow

- Create a project.
- View it in dashboard and project history.
- Open project details.
- Edit the project.
- Delete a test project.

## Estimation Workflow

- Enter manual wall measurements.
- Confirm preview values update.
- Save an estimate.
- Confirm BOQ summary and project details show the estimate.

## Image Workflow

- Pick an image from gallery.
- Capture an image if camera permissions are available.
- Enter a reference measurement.
- Confirm Firebase Storage upload and Firestore image metadata.

## Android UI

- Test on a small portrait Android screen.
- Check keyboard behavior on forms.
- Confirm loading, empty, and error states.
- Confirm button labels and touch targets are readable.
