const ERROR_MESSAGES = {
  "auth/invalid-credential": "Wrong email or password. Please check your details and try again.",
  "auth/user-not-found": "No account found with this email address.",
  "auth/wrong-password": "Wrong password. Please try again.",
  "auth/invalid-email": "Please enter a valid email address.",
  "auth/email-already-in-use": "An account already exists with this email address.",
  "auth/weak-password": "Use a stronger password with at least 6 characters.",
  "auth/too-many-requests": "Too many attempts. Please wait a moment before trying again.",
  "auth/network-request-failed": "Network problem. Check your connection and try again.",
  "permission/camera": "Camera permission is required to take project photos.",
  "permission/gallery": "Photo library permission is required to choose project photos.",
  "storage/unauthorized": "You do not have permission to upload this image.",
  "storage/retry-limit-exceeded": "Upload failed because the connection was unstable. Please try again.",
  "storage/canceled": "The image upload was cancelled.",
  "storage/object-not-found": "The uploaded image could not be found. Please try again.",
  "not-found/project": "Project was not found.",
  "image/missing-uri": "No image file was returned. Please try again.",
  "image/upload-failed": "Photo upload failed. Your draft is saved and you can retry.",
  "firebase/missing-config": "SiteSpy is not fully configured on this build. Please contact the app owner.",
  unknown: "Something went wrong. Please try again."
};

function findKnownCode(error) {
  const code = error?.code || error?.name || "";
  if (ERROR_MESSAGES[code]) {
    return code;
  }

  const message = String(error?.message || error || "");
  const match = message.match(/\b(auth|storage|firestore|permission|image)\/[a-z0-9-]+\b/i);
  if (match && ERROR_MESSAGES[match[0]]) {
    return match[0];
  }

  if (/project was not found/i.test(message)) {
    return "not-found/project";
  }
  if (/network|offline|failed to fetch/i.test(message)) {
    return "auth/network-request-failed";
  }
  if (/camera.*permission|permission.*camera/i.test(message)) {
    return "permission/camera";
  }
  if (/base64|cannot read property 'base64'|cannot read property "base64"/i.test(message)) {
    return "image/upload-failed";
  }

  return "unknown";
}

export function getErrorCode(error) {
  return findKnownCode(error);
}

export function toUserMessage(error, fallback = ERROR_MESSAGES.unknown) {
  const code = findKnownCode(error);
  return ERROR_MESSAGES[code] || fallback;
}

export function logAndGetUserMessage(error, context = "Operation failed", fallback) {
  console.error(`[SiteSpy] ${context}`, {
    code: error?.code || error?.name || "unknown",
    message: error?.message || String(error)
  });
  return toUserMessage(error, fallback);
}
