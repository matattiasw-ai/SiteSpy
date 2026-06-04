import { Ionicons } from "@expo/vector-icons";
import { Pressable, StyleSheet, Text, View } from "react-native";
import AppCard from "./AppCard";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { typography } from "../theme/typography";

export default function ActionCard({ icon = "radio-outline", title, subtitle, onPress, tone = "primary", style }) {
  const iconColor = tone === "accent" ? colors.accent : colors.primary;

  return (
    <Pressable onPress={onPress} style={({ pressed }) => [pressed && styles.pressed, style]}>
      <AppCard variant={tone === "primary" ? "accent" : "default"} style={styles.card}>
        <View style={[styles.iconWrap, tone === "accent" && styles.accentIcon]}>
          <Ionicons name={icon} size={22} color={iconColor} />
        </View>
        <View style={styles.copy}>
          <Text style={styles.title}>{title}</Text>
          {!!subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
        </View>
        <Ionicons name="chevron-forward" size={20} color={colors.muted} />
      </AppCard>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  pressed: {
    opacity: 0.82
  },
  card: {
    minHeight: 92,
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md
  },
  iconWrap: {
    width: 44,
    height: 44,
    borderRadius: spacing.controlRadius,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: colors.primarySoft
  },
  accentIcon: {
    backgroundColor: colors.accentSoft
  },
  copy: {
    flex: 1,
    gap: spacing.xs
  },
  title: {
    color: colors.text,
    fontWeight: "900",
    fontSize: typography.h3
  },
  subtitle: {
    color: colors.muted,
    lineHeight: typography.tightLineHeight
  }
});
