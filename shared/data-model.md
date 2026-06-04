# SiteSpy Data Model

## users

- `userId`: Firebase Auth uid.
- `email`: account email.
- `displayName`: optional profile name.
- `phoneNumber`: optional contact number.
- `discipline`: optional student or user discipline.
- `createdAt`: server timestamp.
- `updatedAt`: server timestamp.

## projects

- `projectId`: Firestore document id.
- `userId`: owner uid.
- `title`: project title.
- `description`: optional notes.
- `location`: optional site location.
- `createdAt`: server timestamp.
- `updatedAt`: server timestamp.

## estimations

- `estimationId`: Firestore document id.
- `projectId`: linked project.
- `userId`: owner uid.
- `wallLength`, `wallHeight`, `wallArea`: wall measurements in metres and square metres.
- `unitType`, `unitLength`, `unitHeight`: brick or block dimensions.
- `estimatedUnits`: estimated masonry unit quantity including waste.
- `mortarQuantity`: simple mortar volume allowance.
- `unitPrice`, `mortarPrice`, `labourRate`: costing inputs.
- `materialCost`, `mortarCost`, `labourCost`, `totalCost`: calculated costs.
- `boqSummary`: report-ready line items.
- `createdAt`: server timestamp.
- `updatedAt`: server timestamp.

## wallImages

- `imageId`: Firestore document id.
- `projectId`: linked project.
- `userId`: owner uid.
- `imageUrl`: Firebase Storage download URL when Storage upload succeeds.
- `storagePath`: optional path under `wallImages/{userId}/`.
- `imageDataUrl`: compressed Firestore image data URL for fallback.
- `width`, `height`: compressed fallback image dimensions.
- `byteEstimate`: approximate compressed fallback image byte size.
- `referenceMeasurement`: user-entered reference length in metres.
- `createdAt`: server timestamp.
- `uploadedAt`: compatibility timestamp for existing image lists.
