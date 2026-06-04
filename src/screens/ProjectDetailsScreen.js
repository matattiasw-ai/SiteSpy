import { useCallback, useState } from "react";
import { Alert, Image, StyleSheet, Text, View } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import AppHeader from "../components/AppHeader";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import CostBreakdownCard from "../components/CostBreakdownCard";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import ListItemCard from "../components/ListItemCard";
import LoadingState from "../components/LoadingState";
import Screen from "../components/Screen";
import SectionHeader from "../components/SectionHeader";
import { useAuth } from "../services/authContext";
import { setActiveProject, setLastRoute } from "../services/localStateService";
import { deleteProject, getProject, listEstimations, listWallImages } from "../services/projectService";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { logAndGetUserMessage } from "../utils/errorMessages";
import { formatDate } from "../utils/formatters";

export default function ProjectDetailsScreen({ route, navigation }) {
  const { projectId } = route.params;
  const { user } = useAuth();
  const [project, setProject] = useState(null);
  const [estimations, setEstimations] = useState([]);
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try {
      setError("");
      const [nextProject, nextEstimations, nextImages] = await Promise.all([
        getProject(projectId),
        listEstimations(user.uid, projectId),
        listWallImages(user.uid, projectId)
      ]);
      setProject(nextProject);
      await setActiveProject(user.uid, { projectId, title: nextProject.title });
      await setLastRoute(user.uid, { name: "ProjectDetails", projectId });
      setEstimations(nextEstimations);
      setImages(nextImages);
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Project details load failed"));
    } finally {
      setLoading(false);
    }
  }, [projectId, user]);

  useFocusEffect(useCallback(() => {
    load();
  }, [load]));

  function confirmDelete() {
    Alert.alert("Delete project", "This removes the project record from your workspace. Saved estimate history may still be available for review.", [
      { text: "Cancel", style: "cancel" },
      {
        text: "Delete",
        style: "destructive",
        onPress: async () => {
          await deleteProject(projectId);
          navigation.goBack();
        }
      }
    ]);
  }

  if (loading) {
    return <Screen><LoadingState message="Loading project details" /></Screen>;
  }

  if (error) {
    return <Screen><ErrorState message={error} onRetry={load} /></Screen>;
  }

  return (
    <Screen>
      <AppHeader
        kicker="Project file"
        title={project.title}
        subtitle={project.description || "No description recorded."}
      />
      <AppCard variant="accent" style={styles.header}>
        <Text style={styles.kicker}>Project file</Text>
        {!!project.location && <Text style={styles.location}>{project.location}</Text>}
        <Text style={styles.date}>Updated {formatDate(project.updatedAt || project.createdAt)}</Text>
      </AppCard>
      <View style={styles.actions}>
        <AppButton title="Manual estimate" icon="calculator-outline" onPress={() => navigation.navigate("ManualEstimate", { projectId, projectTitle: project.title })} />
        <AppButton title="Image-assisted estimate" icon="camera-outline" variant="secondary" onPress={() => navigation.navigate("ImageEstimate", { projectId })} />
        <AppButton title="Edit project" icon="create-outline" variant="secondary" onPress={() => navigation.navigate("EditProject", { projectId })} />
        <AppButton title="Delete project" icon="trash-outline" variant="danger" onPress={confirmDelete} />
      </View>
      <SectionHeader title="Latest estimates" subtitle="Most recent cost records for this project." />
      {estimations.length ? estimations.slice(0, 3).map((estimate) => (
        <CostBreakdownCard key={estimate.id} estimate={estimate} />
      )) : (
        <EmptyState title="No estimates saved" message="Add a manual wall estimate to build the project cost history." />
      )}
      <SectionHeader title="Wall images" subtitle="Reference images captured on site." />
      {images.length ? images.map((image) => (
        <ListItemCard key={image.id} title="Wall reference image" icon="image-outline" style={styles.imageCard}>
          <Image source={{ uri: image.downloadURL || image.imageUrl || image.localUri }} style={styles.image} />
          <Text style={styles.description}>Reference measurement: {image.referenceMeasurement} m</Text>
          {!!image.size && <Text style={styles.description}>Image size: {Math.round(image.size / 1024)} KB</Text>}
        </ListItemCard>
      )) : (
        <EmptyState title="No wall images" message="Image-assisted records will appear here after upload." icon="image-outline" />
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  header: {
    marginBottom: spacing.md
  },
  kicker: {
    color: colors.accent,
    fontWeight: "900",
    textTransform: "uppercase",
    marginBottom: spacing.xs
  },
  description: {
    marginVertical: spacing.sm,
    color: colors.muted,
    lineHeight: 21
  },
  date: {
    color: colors.primary,
    fontWeight: "700"
  },
  location: {
    color: colors.text,
    fontWeight: "800",
    marginBottom: spacing.sm
  },
  actions: {
    gap: spacing.md,
    marginBottom: spacing.lg
  },
  imageCard: {
    marginBottom: spacing.md
  },
  image: {
    width: "100%",
    height: 190,
    borderRadius: spacing.cardRadius,
    backgroundColor: colors.surfaceAlt
  }
});
