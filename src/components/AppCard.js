import { StyleSheet, View } from "react-native";
import { colors } from "../theme/colors";
import { shadows } from "../theme/shadows";
import { spacing } from "../theme/spacing";

export default function AppCard({ children, style, variant = "default" }) {
  return <View style={[styles.card, variant === "muted" && styles.muted, variant === "accent" && styles.accent, style]}>{children}</View>;
}

const styles = StyleSheet.create({
  card: {
    borderWidth: 1,
    borderColor: colors.borderSoft,
    borderRadius: spacing.cardRadius,
    padding: spacing.lg,
    backgroundColor: colors.surface,
    ...shadows.card
  },
  muted: {
    backgroundColor: colors.surfaceAlt
  },
  accent: {
    borderColor: colors.primaryDark,
    backgroundColor: colors.primarySoft
  }
});
