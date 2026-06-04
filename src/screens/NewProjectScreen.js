import { useState } from "react";
import { StyleSheet } from "react-native";
import AppHeader from "../components/AppHeader";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import AppInput from "../components/AppInput";
import ErrorState from "../components/ErrorState";
import Screen from "../components/Screen";
import { useAuth } from "../services/authContext";
import { setActiveProject, setLastRoute } from "../services/localStateService";
import { createProject } from "../services/projectService";
import { spacing } from "../theme/spacing";
import { logAndGetUserMessage } from "../utils/errorMessages";
import { requireText } from "../utils/validators";

export default function NewProjectScreen({ navigation }) {
  const { user } = useAuth();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleCreate() {
    const validation = requireText(title, "Project title");
    if (validation) {
      setError(validation);
      return;
    }
    setLoading(true);
    setError("");
    try {
      const project = await createProject(user.uid, { title, description, location });
      await setActiveProject(user.uid, { projectId: project.id, title });
      await setLastRoute(user.uid, { name: "ManualEstimate", projectId: project.id });
      setTitle("");
      setDescription("");
      setLocation("");
      navigation.navigate("ManualEstimate", { projectId: project.id, projectTitle: title });
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Project creation failed"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <Screen>
      <AppHeader
        kicker="New field file"
        title="Start a wall estimate"
        subtitle="Create a project first, then add manual measurements or an image-assisted record."
      />
      <AppCard style={styles.form}>
        {!!error && <ErrorState message={error} />}
        <AppInput label="Project title" value={title} onChangeText={setTitle} placeholder="Boundary wall estimate" />
        <AppInput
          label="Description"
          value={description}
          onChangeText={setDescription}
          placeholder="Site, client, or construction notes"
          multiline
        />
        <AppInput label="Location (optional)" value={location} onChangeText={setLocation} placeholder="Windhoek, Katutura site" />
        <AppButton title="Create and estimate" icon="calculator-outline" onPress={handleCreate} loading={loading} />
      </AppCard>
    </Screen>
  );
}

const styles = StyleSheet.create({
  form: {
    gap: spacing.md
  }
});
