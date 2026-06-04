import { useState } from "react";
import { Switch, StyleSheet, Text, View } from "react-native";
import AppHeader from "../components/AppHeader";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import Screen from "../components/Screen";
import { logout } from "../services/authService";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export default function SettingsScreen() {
  const [metricUnits, setMetricUnits] = useState(true);
  const [saveDrafts, setSaveDrafts] = useState(true);

  return (
    <Screen>
      <AppHeader
        kicker="Controls"
        title="Settings"
        subtitle="Draft settings for field estimation preferences."
      />
      <AppCard style={styles.card}>
        <SettingRow label="Use metric units" value={metricUnits} onValueChange={setMetricUnits} />
        <SettingRow label="Save calculation drafts" value={saveDrafts} onValueChange={setSaveDrafts} />
      </AppCard>
      <AppCard style={styles.card}>
        <Text style={styles.sectionTitle}>App details</Text>
        <Text style={styles.detail}>Optimized for Android field use.</Text>
        <Text style={styles.detail}>Version 0.7.0</Text>
      </AppCard>
      <AppButton title="Log out" icon="log-out-outline" variant="danger" onPress={logout} />
    </Screen>
  );
}

function SettingRow({ label, value, onValueChange }) {
  return (
    <View style={styles.row}>
      <Text style={styles.rowLabel}>{label}</Text>
      <Switch
        value={value}
        onValueChange={onValueChange}
        trackColor={{ false: colors.border, true: colors.primary }}
        thumbColor={colors.surface}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    gap: spacing.md,
    marginBottom: spacing.md
  },
  row: {
    minHeight: 54,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: spacing.md
  },
  rowLabel: {
    flex: 1,
    color: colors.text,
    fontWeight: "800"
  },
  sectionTitle: {
    color: colors.text,
    fontWeight: "900",
    fontSize: 18
  },
  detail: {
    color: colors.muted,
    lineHeight: 21
  }
});
