import { Ionicons } from "@expo/vector-icons";
import { Pressable, StyleSheet, Text, View } from "react-native";
import AppCard from "./AppCard";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { typography } from "../theme/typography";

export default function ListItemCard({ kicker, title, subtitle, meta, icon = "document-text-outline", onPress, children, style }) {
  const content = (
    <AppCard style={[styles.card, style]}>
      <View style={styles.iconWrap}>
        <Ionicons name={icon} size={20} color={colors.primary} />
      </View>
      <View style={styles.copy}>
        {!!kicker && <Text style={styles.kicker}>{kicker}</Text>}
        <Text style={styles.title}>{title}</Text>
        {!!subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
        {!!meta && <Text style={styles.meta}>{meta}</Text>}
        {children}
      </View>
      {!!onPress && <Ionicons name="chevron-forward" size={20} color={colors.mutedSoft} />}
    </AppCard>
  );

  if (!onPress) {
    return content;
  }

  return (
    <Pressable onPress={onPress} style={({ pressed }) => pressed && styles.pressed}>
      {content}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  pressed: {
    opacity: 0.84
  },
  card: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
    marginBottom: spacing.md
  },
  iconWrap: {
    width: 40,
    height: 40,
    borderRadius: spacing.controlRadius,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: colors.primarySoft
  },
  copy: {
    flex: 1,
    gap: spacing.xs
  },
  kicker: {
    color: colors.accent,
    fontWeight: "900",
    fontSize: typography.small,
    textTransform: "uppercase"
  },
  title: {
    color: colors.text,
    fontWeight: "900",
    fontSize: typography.h3
  },
  subtitle: {
    color: colors.muted,
    lineHeight: typography.lineHeight
  },
  meta: {
    color: colors.primary,
    fontWeight: "800"
  }
});
