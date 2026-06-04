import { StyleSheet, Text, TextInput, View } from "react-native";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { typography } from "../theme/typography";

export default function AppInput({ label, helperText, error, style, inputStyle, ...props }) {
  return (
    <View style={[styles.wrap, style]}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        placeholderTextColor={colors.muted}
        style={[styles.input, props.multiline && styles.multiline, error && styles.inputError, inputStyle]}
        {...props}
      />
      {!!helperText && !error && <Text style={styles.helper}>{helperText}</Text>}
      {!!error && <Text style={styles.error}>{error}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
    gap: spacing.sm
  },
  label: {
    color: colors.muted,
    fontWeight: "800",
    fontSize: typography.label,
    textTransform: "uppercase"
  },
  input: {
    minHeight: spacing.inputHeight,
    borderWidth: 1,
    borderColor: colors.borderSoft,
    borderRadius: spacing.controlRadius,
    paddingHorizontal: spacing.md,
    color: colors.text,
    backgroundColor: colors.surfaceAlt,
    fontSize: typography.body
  },
  multiline: {
    minHeight: 104,
    paddingTop: spacing.md,
    textAlignVertical: "top"
  },
  inputError: {
    borderColor: colors.danger
  },
  helper: {
    color: colors.mutedSoft,
    fontSize: typography.small
  },
  error: {
    color: colors.danger,
    fontSize: 13
  }
});
