import { StyleSheet, Text, View } from "react-native";
import AppCard from "./AppCard";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { formatCurrency } from "../utils/formatters";

export default function CostBreakdownCard({ estimate }) {
  if (!estimate) return null;

  const rows = [
    ["Masonry units", formatCurrency(estimate.materialCost)],
    ["Mortar allowance", formatCurrency(estimate.mortarCost)],
    ["Labour", formatCurrency(estimate.labourCost)]
  ];

  return (
    <AppCard>
      <Text style={styles.kicker}>BOQ</Text>
      <Text style={styles.title}>Cost breakdown</Text>
      {rows.map(([label, value]) => (
        <View key={label} style={styles.row}>
          <Text style={styles.label}>{label}</Text>
          <Text style={styles.value}>{value}</Text>
        </View>
      ))}
      <View style={styles.total}>
        <Text style={styles.totalLabel}>Project estimate</Text>
        <Text style={styles.totalValue}>{formatCurrency(estimate.totalCost)}</Text>
      </View>
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
    paddingVertical: spacing.sm
  },
  label: {
    color: colors.muted
  },
  value: {
    color: colors.text,
    fontWeight: "700"
  },
  total: {
    marginTop: spacing.md,
    paddingTop: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.borderSoft,
    gap: spacing.xs
  },
  totalLabel: {
    color: colors.muted
  },
  totalValue: {
    color: colors.primary,
    fontWeight: "900",
    fontSize: 24
  }
});
