import { StyleSheet, Text, View } from "react-native";
import { buildInfo, firebaseConfigFlags, missingFirebaseConfigKeys } from "../services/runtimeConfig";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { typography } from "../theme/typography";

export default function RuntimeConfigDiagnosticScreen() {
  return (
    <View style={styles.wrap}>
      <Text style={styles.kicker}>SiteSpy runtime diagnostic</Text>
      <Text style={styles.title}>App setup is incomplete</Text>
      <Text style={styles.body}>
        This preview build cannot start because required public app settings were not bundled.
      </Text>
      <Text style={styles.label}>Setup status</Text>
      <Text style={styles.value}>{missingFirebaseConfigKeys.length ? "Required app settings are unavailable." : "Ready"}</Text>
      <Text style={styles.label}>Build</Text>
      <Text style={styles.value}>
        {buildInfo.appName} {buildInfo.appVersion} / {buildInfo.platform} / {buildInfo.appEnvironment || "unknown"}
      </Text>
      <Text style={styles.label}>Setup checks</Text>
      <Text style={styles.value}>{JSON.stringify(firebaseConfigFlags, null, 2)}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    flex: 1,
    justifyContent: "center",
    padding: spacing.screen,
    backgroundColor: colors.background
  },
  kicker: {
    color: colors.primary,
    fontWeight: "900",
    marginBottom: spacing.sm,
    textTransform: "uppercase"
  },
  title: {
    color: colors.text,
    fontSize: typography.h2,
    fontWeight: "900",
    marginBottom: spacing.md
  },
  body: {
    color: colors.muted,
    lineHeight: typography.lineHeight,
    marginBottom: spacing.lg
  },
  label: {
    color: colors.accent,
    fontWeight: "900",
    marginTop: spacing.md
  },
  value: {
    color: colors.text,
    lineHeight: 21,
    marginTop: spacing.xs
  }
});
