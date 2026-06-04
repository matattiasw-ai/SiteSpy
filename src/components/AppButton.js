import { Ionicons } from "@expo/vector-icons";
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from "react-native";
import { colors } from "../theme/colors";
import { shadows } from "../theme/shadows";
import { spacing } from "../theme/spacing";
import { typography } from "../theme/typography";

export default function AppButton({ title, onPress, variant = "primary", loading = false, disabled = false, icon, style }) {
  const isSecondary = variant === "secondary";
  const isDanger = variant === "danger";
  const isGhost = variant === "ghost";
  const foreground = isSecondary || isGhost || isDanger ? colors.text : colors.background;

  return (
    <Pressable
      onPress={onPress}
      disabled={disabled || loading}
      style={({ pressed }) => [
        styles.button,
        isSecondary && styles.secondary,
        isDanger && styles.danger,
        isGhost && styles.ghost,
        (disabled || loading) && styles.disabled,
        pressed && styles.pressed,
        style
      ]}
    >
      {loading ? <ActivityIndicator color={isSecondary ? colors.primary : colors.surface} /> : (
        <View style={styles.content}>
          {!!icon && <Ionicons name={icon} size={18} color={foreground} />}
          <Text style={[styles.text, (isSecondary || isGhost) && styles.secondaryText, isDanger && styles.dangerText]}>{title}</Text>
        </View>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    minHeight: spacing.buttonHeight,
    borderRadius: spacing.controlRadius,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: spacing.lg,
    backgroundColor: colors.primary,
    ...shadows.soft
  },
  secondary: {
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.secondarySoft
  },
  danger: {
    backgroundColor: colors.danger
  },
  ghost: {
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: colors.border
  },
  disabled: {
    opacity: 0.55
  },
  pressed: {
    transform: [{ scale: 0.99 }]
  },
  text: {
    color: colors.background,
    fontWeight: "800",
    fontSize: typography.button
  },
  secondaryText: {
    color: colors.text
  },
  dangerText: {
    color: colors.text
  },
  content: {
    minHeight: 24,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.sm
  }
});
