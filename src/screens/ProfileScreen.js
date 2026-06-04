import { StyleSheet, Text, View } from "react-native";
import AppHeader from "../components/AppHeader";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import Screen from "../components/Screen";
import { useAuth } from "../services/authContext";
import { logout } from "../services/authService";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export default function ProfileScreen({ navigation }) {
  const { user } = useAuth();

  return (
    <Screen>
      <AppHeader logo kicker="Account" title="Profile" subtitle="Account and session details." />
      <AppCard style={styles.card}>
        <Text style={styles.kicker}>Signed-in account</Text>
        <Text style={styles.label}>Email</Text>
        <Text style={styles.value}>{user?.email || "Not signed in"}</Text>
        <Text style={styles.label}>User ID</Text>
        <Text style={styles.valueSmall}>{user?.uid || "Not available"}</Text>
      </AppCard>
      <View style={styles.actions}>
        <AppButton title="Settings" icon="settings-outline" variant="secondary" onPress={() => navigation.navigate("Settings")} />
        <AppButton title="Log out" icon="log-out-outline" variant="danger" onPress={logout} />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  card: {
    gap: spacing.sm
  },
  label: {
    color: colors.muted,
    fontWeight: "700"
  },
  kicker: {
    color: colors.accent,
    fontWeight: "900",
    textTransform: "uppercase"
  },
  value: {
    color: colors.text,
    fontWeight: "900",
    fontSize: 18,
    marginBottom: spacing.md
  },
  valueSmall: {
    color: colors.text,
    lineHeight: 21
  },
  actions: {
    gap: spacing.md,
    marginTop: spacing.lg
  }
});
