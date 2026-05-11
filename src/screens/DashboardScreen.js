import { useCallback, useState } from "react";
import { RefreshControl, StyleSheet, Text, View } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import ActionCard from "../components/ActionCard";
import AppHeader from "../components/AppHeader";
import AppCard from "../components/AppCard";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import ListItemCard from "../components/ListItemCard";
import LoadingState from "../components/LoadingState";
import Screen from "../components/Screen";
import SectionHeader from "../components/SectionHeader";
import StatCard from "../components/StatCard";
import { useAuth } from "../services/authContext";
import { listEstimations, listProjects } from "../services/projectService";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { logAndGetUserMessage } from "../utils/errorMessages";
import { formatCurrency, formatDate } from "../utils/formatters";

export default function DashboardScreen({ navigation }) {
  const { user } = useAuth();
  const { localContext, refreshLocalContext } = useAuth();
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");
  const [projects, setProjects] = useState([]);
  const [estimations, setEstimations] = useState([]);

  const load = useCallback(async () => {
    if (!user) return;
    setError("");
    try {
      const nextProjects = await listProjects(user.uid);
      const allEstimations = [];
      for (const project of nextProjects) {
        const projectEstimations = await listEstimations(user.uid, project.id);
        allEstimations.push(...projectEstimations);
      }
      setProjects(nextProjects);
      setEstimations(allEstimations);
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Dashboard load failed"));
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [user]);

  useFocusEffect(useCallback(() => {
    load();
    refreshLocalContext(user);
  }, [load]));

  const totalCost = estimations.reduce((sum, item) => sum + Number(item.totalCost || 0), 0);
  const totalUnits = estimations.reduce((sum, item) => sum + Number(item.estimatedUnits || 0), 0);

  if (loading) {
    return <Screen><LoadingState message="Loading dashboard" /></Screen>;
  }

  return (
    <Screen
      scroll
      padded
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={() => { setRefreshing(true); load(); }} />}
    >
      <AppHeader
        logo
        kicker="Field intelligence"
        title="Project dashboard"
        subtitle="Track wall estimates, quantities, images, and labour costs."
      />
      {!!error && <ErrorState message={error} onRetry={load} />}
      {!!localContext?.activeProject?.projectId && (
        <AppCard variant="muted" style={styles.resumeCard}>
          <Text style={styles.resumeTitle}>Continue your last project?</Text>
          <Text style={styles.resumeText}>{localContext.activeProject.title || "Unfinished project workflow"}</Text>
          {!!localContext.pendingUploads?.length && (
            <Text style={styles.resumeText}>{localContext.pendingUploads.length} pending image upload draft saved locally.</Text>
          )}
          <AppButton
            title="Continue"
            icon="play-forward-outline"
            onPress={() => navigation.navigate("Projects", {
              screen: "ProjectDetails",
              params: { projectId: localContext.activeProject.projectId }
            })}
          />
        </AppCard>
      )}
      <AppCard variant="accent" style={styles.welcomeCard}>
        <Text style={styles.welcomeTitle}>Ready for site measurements</Text>
        <Text style={styles.welcomeText}>Create a project, capture measurements, and keep every BOQ estimate tied to your account.</Text>
      </AppCard>
      <View style={styles.metrics}>
        <StatCard label="Projects" value={projects.length} icon="folder-open-outline" />
        <StatCard label="Estimations" value={estimations.length} icon="calculator-outline" />
        <StatCard label="Masonry units" value={totalUnits} icon="cube-outline" />
        <StatCard label="Total estimate" value={formatCurrency(totalCost)} icon="cash-outline" />
      </View>
      <View style={styles.actions}>
        <ActionCard
          icon="add-circle-outline"
          title="New project"
          subtitle="Create a field file and start an estimate."
          onPress={() => navigation.navigate("New", { screen: "NewProject" })}
        />
        <ActionCard
          icon="folder-open-outline"
          title="Project history"
          subtitle="Review saved projects and previous BOQ totals."
          tone="accent"
          onPress={() => navigation.navigate("Projects")}
        />
      </View>
      <SectionHeader title="Recent projects" subtitle="Latest field files saved to your workspace." />
      {projects.length ? projects.slice(0, 4).map((project) => (
        <ListItemCard
          key={project.id}
          kicker="Project"
          title={project.title}
          subtitle={project.description || "No description recorded."}
          meta={`Created ${formatDate(project.createdAt)}`}
          icon="shield-checkmark-outline"
        />
      )) : (
        <EmptyState title="No projects yet" message="Create a project to start calculating wall material and labour costs." />
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  metrics: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.md,
    marginTop: spacing.md
  },
  actions: {
    gap: spacing.md,
    marginVertical: spacing.lg
  },
  welcomeCard: {},
  welcomeTitle: {
    color: colors.text,
    fontWeight: "900",
    fontSize: 19,
    marginBottom: spacing.sm
  },
  welcomeText: {
    color: colors.muted,
    lineHeight: 22
  },
  resumeCard: {
    gap: spacing.md,
    marginBottom: spacing.md
  },
  resumeTitle: {
    color: colors.text,
    fontWeight: "900",
    fontSize: 18
  },
  resumeText: {
    color: colors.muted,
    lineHeight: 21
  }
});
