import { useCallback, useState } from "react";
import { useFocusEffect } from "@react-navigation/native";
import AppHeader from "../components/AppHeader";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import ListItemCard from "../components/ListItemCard";
import LoadingState from "../components/LoadingState";
import Screen from "../components/Screen";
import { useAuth } from "../services/authContext";
import { listProjects } from "../services/projectService";
import { logAndGetUserMessage } from "../utils/errorMessages";
import { formatDate } from "../utils/formatters";

export default function ProjectHistoryScreen({ navigation }) {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try {
      setError("");
      setProjects(await listProjects(user.uid));
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Project history load failed"));
    } finally {
      setLoading(false);
    }
  }, [user]);

  useFocusEffect(useCallback(() => {
    load();
  }, [load]));

  if (loading) {
    return <Screen><LoadingState message="Loading project history" /></Screen>;
  }

  return (
    <Screen>
      <AppHeader
        kicker="Archive"
        title="Project history"
        subtitle="Review saved SiteSpy projects and their estimate records."
      />
      {!!error && <ErrorState message={error} onRetry={load} />}
      {!projects.length && !error ? (
        <EmptyState title="No saved projects" message="New wall projects will appear here in chronological order." />
      ) : projects.map((project) => (
        <ListItemCard
          key={project.id}
          kicker="Project"
          title={project.title}
          subtitle={project.description || "No description recorded."}
          meta={`Updated ${formatDate(project.updatedAt || project.createdAt)}`}
          icon="folder-open-outline"
          onPress={() => navigation.navigate("ProjectDetails", { projectId: project.id })}
        />
      ))}
    </Screen>
  );
}
