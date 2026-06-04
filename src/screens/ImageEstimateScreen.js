import * as ImagePicker from "expo-image-picker";
import { useState } from "react";
import { Image, StyleSheet, Text, View } from "react-native";
import AppHeader from "../components/AppHeader";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import AppInput from "../components/AppInput";
import ErrorState from "../components/ErrorState";
import Screen from "../components/Screen";
import { savePendingUpload, removePendingUpload, setLastRoute } from "../services/localStateService";
import { useAuth } from "../services/authContext";
import { saveWallImage } from "../services/projectService";
import { uploadWallImage } from "../services/storageService";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { prepareImageForUpload } from "../utils/imageUtils";
import { logAndGetUserMessage, toUserMessage } from "../utils/errorMessages";
import { requirePositiveNumber } from "../utils/validators";

export default function ImageEstimateScreen({ route, navigation }) {
  const { projectId } = route.params;
  const { user } = useAuth();
  const [image, setImage] = useState(null);
  const [referenceMeasurement, setReferenceMeasurement] = useState("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [saving, setSaving] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");
  const [pendingDraft, setPendingDraft] = useState(null);

  async function pickImage(source) {
    if (saving) return;
    setError("");
    setNotice("");
    try {
      const permission = source === "camera"
        ? await ImagePicker.requestCameraPermissionsAsync()
        : await ImagePicker.requestMediaLibraryPermissionsAsync();

      if (!permission?.granted) {
        const permissionError = new Error(source === "camera" ? "Camera permission denied." : "Gallery permission denied.");
        permissionError.code = source === "camera" ? "permission/camera" : "permission/gallery";
        setError(toUserMessage(permissionError));
        return;
      }

      const result = source === "camera"
        ? await ImagePicker.launchCameraAsync({ quality: 0.84, allowsEditing: false })
        : await ImagePicker.launchImageLibraryAsync({ quality: 0.84, allowsEditing: false, mediaTypes: ImagePicker.MediaTypeOptions.Images });

      if (!result || result.canceled) {
        return;
      }

      const selected = Array.isArray(result.assets) ? result.assets[0] : null;
      if (!selected?.uri) {
        const missingUriError = new Error("Image picker returned no URI.");
        missingUriError.code = "image/missing-uri";
        setError(toUserMessage(missingUriError));
        return;
      }

      const imageId = `${Date.now()}`;
      const draft = {
        imageId,
        projectId,
        localUri: selected.uri,
        fileName: selected.fileName || `${imageId}.jpg`,
        mimeType: selected.mimeType || "image/jpeg",
        size: selected.fileSize || null,
        status: "pending",
        referenceMeasurement
      };
      setImage({ ...selected, imageId });
      setPendingDraft(draft);
      await savePendingUpload(user.uid, draft);
      await setLastRoute(user.uid, { name: "ImageEstimate", projectId });
      setNotice("Photo draft saved locally. Add a reference measurement and upload when ready.");
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Image selection failed"));
    }
  }

  async function handleSave(draftOverride = null) {
    if (saving) return;
    const activeDraft = draftOverride || pendingDraft;
    const activeImage = image || (activeDraft?.localUri ? { uri: activeDraft.localUri, imageId: activeDraft.imageId } : null);
    if (!activeImage?.uri) {
      const missingImageError = new Error("No image selected.");
      missingImageError.code = "image/missing-uri";
      setError(toUserMessage(missingImageError, "Select or capture a wall image first."));
      return;
    }
    const validation = requirePositiveNumber(referenceMeasurement, "Reference measurement");
    if (validation) {
      setError(validation);
      return;
    }

    setSaving(true);
    setError("");
    setNotice("");
    setUploadStatus("Preparing image...");
    try {
      const prepared = await prepareImageForUpload(activeImage.uri);
      const imageId = activeImage.imageId || activeDraft?.imageId || `${Date.now()}`;
      const draft = {
        ...(activeDraft || {}),
        imageId,
        projectId,
        localUri: prepared.uri,
        referenceMeasurement,
        status: "uploading",
        mimeType: prepared.mimeType,
        width: prepared.width,
        height: prepared.height
      };
      await savePendingUpload(user.uid, draft);
      setUploadStatus("Uploading photo...");
      const uploaded = await uploadWallImage(user.uid, projectId, {
        ...draft,
        uri: prepared.uri
      });
      setUploadStatus("Saving photo record...");
      await saveWallImage(user.uid, projectId, {
        ...uploaded,
        localUri: prepared.uri,
        referenceMeasurement,
        status: "uploaded",
        width: prepared.width,
        height: prepared.height
      });
      await removePendingUpload(user.uid, imageId);
      setUploadStatus("Done");
      navigation.navigate("ProjectDetails", { projectId });
    } catch (nextError) {
      const failedDraft = {
        ...(activeDraft || {}),
        imageId: activeImage.imageId || activeDraft?.imageId || `${Date.now()}`,
        projectId,
        localUri: activeImage.uri,
        referenceMeasurement,
        status: "failed"
      };
      await savePendingUpload(user.uid, failedDraft);
      setPendingDraft(failedDraft);
      setError(logAndGetUserMessage(nextError, "Image upload failed", "Photo upload failed. Your draft is saved and you can retry."));
    } finally {
      setSaving(false);
      setUploadStatus("");
    }
  }

  return (
    <Screen>
      <AppHeader
        kicker="Image record"
        title="Image-assisted record"
        subtitle="Attach a wall photo and reference measurement. SiteSpy will save the photo with this estimate for project records."
      />
      {!!error && <ErrorState message={error} />}
      {!!notice && <Text style={styles.notice}>{notice}</Text>}
      {!!uploadStatus && <Text style={styles.notice}>{uploadStatus}</Text>}
      <AppCard style={styles.imagePanel}>
        <View style={styles.actions}>
          <AppButton title="Use camera" icon="camera-outline" onPress={() => pickImage("camera")} />
          <AppButton title="Choose from gallery" icon="images-outline" variant="secondary" onPress={() => pickImage("gallery")} />
        </View>
        {image ? <Image source={{ uri: image.uri }} style={styles.preview} /> : (
          <View style={styles.placeholder}>
            <Text style={styles.placeholderText}>No image selected</Text>
          </View>
        )}
        <AppInput
          label="Reference measurement (m)"
          value={referenceMeasurement}
          onChangeText={setReferenceMeasurement}
          keyboardType="decimal-pad"
          placeholder="Example: 2.4"
        />
        <AppButton title="Save photo record" icon="cloud-upload-outline" onPress={() => handleSave()} loading={saving} disabled={saving} />
        {!!pendingDraft && pendingDraft.status === "failed" && (
          <AppButton title="Retry saved draft" icon="refresh-outline" variant="secondary" onPress={() => handleSave(pendingDraft)} loading={saving} disabled={saving} />
        )}
      </AppCard>
    </Screen>
  );
}

const styles = StyleSheet.create({
  actions: {
    gap: spacing.md,
    marginBottom: spacing.md
  },
  imagePanel: {
    gap: spacing.md
  },
  preview: {
    width: "100%",
    height: 260,
    borderRadius: spacing.cardRadius,
    marginBottom: spacing.md
  },
  placeholder: {
    height: 220,
    borderWidth: 1,
    borderColor: colors.borderSoft,
    borderRadius: spacing.cardRadius,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: spacing.md,
    backgroundColor: colors.surfaceAlt
  },
  placeholderText: {
    color: colors.muted,
    fontWeight: "700"
  },
  notice: {
    color: colors.success,
    fontWeight: "800",
    marginBottom: spacing.md,
    padding: spacing.md,
    borderRadius: spacing.cardRadius,
    backgroundColor: colors.successSurface
  }
});
