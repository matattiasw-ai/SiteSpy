import { StyleSheet, Text, View } from "react-native";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { typography } from "../theme/typography";

export default function SectionHeader({ title, subtitle, action }) {
  return (
    <View style={styles.wrap}>
      <View style={styles.copy}>
        <Text style={styles.title}>{title}</Text>
        {!!subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
      </View>
      {action}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: spacing.md,
    marginBottom: spacing.md
  },
  copy: {
    flex: 1,
    gap: spacing.xs
  },
  title: {
    color: colors.text,
    fontWeight: "900",
    fontSize: typography.h2
  },
  subtitle: {
    color: colors.muted,
    lineHeight: typography.lineHeight
  }
});
