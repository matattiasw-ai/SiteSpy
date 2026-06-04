import * as ImageManipulator from "expo-image-manipulator";

export async function prepareImageForUpload(imageUri) {
  if (!imageUri) {
    const error = new Error("No image URI was provided.");
    error.code = "image/missing-uri";
    throw error;
  }

  const result = await ImageManipulator.manipulateAsync(
    imageUri,
    [{ resize: { width: 1400 } }],
    { compress: 0.78, format: ImageManipulator.SaveFormat.JPEG }
  );

  return {
    uri: result.uri,
    width: result.width,
    height: result.height,
    mimeType: "image/jpeg"
  };
}
