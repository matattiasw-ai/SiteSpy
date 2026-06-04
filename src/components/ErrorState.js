import { StyleSheet, Text, View } from "react-native";
import AppButton from "./AppButton";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export default function ErrorState({ message, onRetry }) {
  return (
    <View style={styles.wrap}>
      <Text style={styles.title}>Something needs attention</Text>
      <Text style={styles.message}>{message}</Text>
      {!!onRetry && <AppButton title="Try again" onPress={onRetry} variant="secondary" />}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    gap: spacing.md,
    padding: spacing.lg,
    borderRadius: spacing.cardRadius,
    borderWidth: 1,
    borderColor: colors.danger,
    backgroundColor: colors.dangerSurface
  },
  title: {
    color: colors.danger,
    fontWeight: "800",
    fontSize: 17
  },
  message: {
    color: colors.text,
    lineHeight: 21
  }
});
