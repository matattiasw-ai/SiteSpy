import { Image, StyleSheet, Text, View } from "react-native";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { typography } from "../theme/typography";

export default function AppHeader({ kicker, title, subtitle, logo = false, centered = false, style }) {
  return (
    <View style={[styles.wrap, centered && styles.centered, style]}>
      {logo && <Image source={require("../../assets/logo-mark-transparent.png")} style={centered ? styles.logoLarge : styles.logo} resizeMode="contain" />}
      {!!kicker && <Text style={styles.kicker}>{kicker}</Text>}
      <Text style={[styles.title, centered && styles.centeredText]}>{title}</Text>
      {!!subtitle && <Text style={[styles.subtitle, centered && styles.centeredText]}>{subtitle}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    gap: spacing.sm,
    marginBottom: spacing.lg
  },
  centered: {
    alignItems: "center",
    marginBottom: spacing.xl
  },
  logo: {
    width: 52,
    height: 52,
    marginBottom: spacing.xs
  },
  logoLarge: {
    width: 96,
    height: 96,
    marginBottom: spacing.sm
  },
  kicker: {
    color: colors.primary,
    fontWeight: "900",
    textTransform: "uppercase"
  },
  title: {
    color: colors.text,
    fontWeight: "900",
    fontSize: typography.title,
    lineHeight: 34
  },
  subtitle: {
    color: colors.muted,
    fontSize: typography.body,
    lineHeight: typography.lineHeight
  },
  centeredText: {
    textAlign: "center"
  }
});
