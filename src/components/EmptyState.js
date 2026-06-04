import { Ionicons } from "@expo/vector-icons";
import { StyleSheet, Text, View } from "react-native";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export default function EmptyState({ title, message, icon = "file-tray-outline" }) {
  return (
    <View style={styles.wrap}>
      <Ionicons name={icon} size={36} color={colors.muted} />
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.message}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    alignItems: "center",
    gap: spacing.sm,
    padding: spacing.xl,
    borderRadius: spacing.cardRadius,
    borderWidth: 1,
    borderColor: colors.borderSoft,
    backgroundColor: colors.surface
  },
  title: {
    color: colors.text,
    fontWeight: "800",
    fontSize: 18
  },
  message: {
    color: colors.muted,
    textAlign: "center",
    lineHeight: 21
  }
});
