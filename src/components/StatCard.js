import { Ionicons } from "@expo/vector-icons";
import { StyleSheet, Text, View } from "react-native";
import AppCard from "./AppCard";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export default function StatCard({ label, value, icon = "analytics-outline", style }) {
  return (
    <AppCard style={[styles.card, style]}>
      <View style={styles.top}>
        <Text style={styles.label}>{label}</Text>
        <Ionicons name={icon} size={18} color={colors.primary} />
      </View>
      <Text style={styles.value} numberOfLines={2}>{value}</Text>
    </AppCard>
  );
}

const styles = StyleSheet.create({
  card: {
    flexBasis: "47%",
    flexGrow: 1,
    minHeight: 112
  },
  top: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: spacing.sm
  },
  label: {
    color: colors.muted,
    fontWeight: "800"
  },
  value: {
    marginTop: spacing.sm,
    color: colors.text,
    fontWeight: "900",
    fontSize: 24
  }
});
