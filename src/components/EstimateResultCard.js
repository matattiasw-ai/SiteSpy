import { StyleSheet, Text, View } from "react-native";
import AppCard from "./AppCard";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { formatCurrency, formatNumber } from "../utils/formatters";

export default function EstimateResultCard({ estimate }) {
  if (!estimate) return null;

  const rows = [
    ["Wall area", `${formatNumber(estimate.wallArea)} m2`],
    ["Estimated units", estimate.estimatedUnits],
    ["Mortar quantity", `${formatNumber(estimate.mortarQuantity, 3)} m3`],
    ["Total cost", formatCurrency(estimate.totalCost)]
  ];

  return (
    <AppCard>
      <Text style={styles.kicker}>Calculated output</Text>
      <Text style={styles.title}>Estimate result</Text>
      {rows.map(([label, value]) => (
        <View key={label} style={styles.row}>
          <Text style={styles.label}>{label}</Text>
          <Text style={styles.value}>{value}</Text>
        </View>
      ))}
    </AppCard>
  );
}

const styles = StyleSheet.create({
  title: {
    color: colors.text,
    fontWeight: "900",
    fontSize: 18,
    marginBottom: spacing.md
  },
  kicker: {
    color: colors.accent,
    fontSize: 12,
    fontWeight: "900",
    textTransform: "uppercase",
    marginBottom: spacing.xs
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: spacing.md,
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.borderSoft
  },
  label: {
    color: colors.muted
  },
  value: {
    color: colors.text,
    fontWeight: "900",
    textAlign: "right"
  }
});
