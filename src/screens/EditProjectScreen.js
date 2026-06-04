import { useEffect, useState } from "react";
import { StyleSheet, Text } from "react-native";
import AppHeader from "../components/AppHeader";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import AppInput from "../components/AppInput";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import Screen from "../components/Screen";
import { getProject, updateProject } from "../services/projectService";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { logAndGetUserMessage } from "../utils/errorMessages";
import { requireText } from "../utils/validators";

export default function EditProjectScreen({ route, navigation }) {
  const { projectId } = route.params;
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getProject(projectId)
      .then((project) => {
        setTitle(project.title);
        setDescription(project.description || "");
        setLocation(project.location || "");
      })
      .catch((nextError) => setError(logAndGetUserMessage(nextError, "Project load failed")))
      .finally(() => setLoading(false));
  }, [projectId]);

  async function handleSave() {
    const validation = requireText(title, "Project title");
    if (validation) {
      setError(validation);
      return;
    }
    setSaving(true);
    setError("");
    try {
      await updateProject(projectId, { title, description, location });
      navigation.goBack();
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Project update failed"));
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return <Screen><LoadingState message="Loading project" /></Screen>;
  }

  return (
    <Screen>
      <AppHeader
        kicker="Project settings"
        title="Edit project"
        subtitle="Update the visible project details used across estimates and history."
      />
      <AppCard style={styles.form}>
        <Text style={styles.title}>Project basics</Text>
        {!!error && <ErrorState message={error} />}
        <AppInput label="Title" value={title} onChangeText={setTitle} />
        <AppInput label="Description" value={description} onChangeText={setDescription} multiline />
        <AppInput label="Location (optional)" value={location} onChangeText={setLocation} />
        <AppButton title="Save changes" icon="save-outline" onPress={handleSave} loading={saving} />
      </AppCard>
    </Screen>
  );
}

const styles = StyleSheet.create({
  form: {
    gap: spacing.md
  },
  title: {
    color: colors.text,
    fontWeight: "900",
    fontSize: 24
  }
});
