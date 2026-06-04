import { StyleSheet, Text, View } from "react-native";
import AppHeader from "../components/AppHeader";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import CostBreakdownCard from "../components/CostBreakdownCard";
import EstimateResultCard from "../components/EstimateResultCard";
import Screen from "../components/Screen";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export default function EstimateSummaryScreen({ route, navigation }) {
  const { estimate, projectId } = route.params;

  return (
    <Screen>
      <AppHeader
        kicker="Measured result"
        title="BOQ estimate summary"
        subtitle="Saved to this project and ready for history review."
      />
      <EstimateResultCard estimate={estimate} />
      <CostBreakdownCard estimate={estimate} />
      <AppCard>
        <Text style={styles.cardTitle}>Measurement basis</Text>
        <Text style={styles.detail}>Unit type: {estimate.unitType}</Text>
        <Text style={styles.detail}>Unit size: {estimate.unitLength} m x {estimate.unitHeight} m</Text>
        <Text style={styles.detail}>Wall size: {estimate.wallLength} m x {estimate.wallHeight} m</Text>
      </AppCard>
      <View style={styles.actions}>
        <AppButton title="Back to project" icon="arrow-back-outline" onPress={() => navigation.navigate("ProjectDetails", { projectId })} />
        <AppButton title="Project history" icon="folder-open-outline" variant="secondary" onPress={() => navigation.navigate("ProjectHistory")} />
        <AppButton title="Share/export coming soon" variant="ghost" disabled />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  cardTitle: {
    color: colors.text,
    fontWeight: "900",
    fontSize: 18,
    marginBottom: spacing.sm
  },
  detail: {
    color: colors.muted,
    marginBottom: spacing.xs
  },
  actions: {
    gap: spacing.md,
    marginTop: spacing.lg
  }
});
