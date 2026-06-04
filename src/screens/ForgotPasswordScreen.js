import { useState } from "react";
import { StyleSheet, Text } from "react-native";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import AppInput from "../components/AppInput";
import AuthScreenContainer from "../components/AuthScreenContainer";
import BrandHeader from "../components/BrandHeader";
import ErrorState from "../components/ErrorState";
import { sendPasswordlessSignInLink, sendPasswordReset } from "../services/authService";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { logAndGetUserMessage } from "../utils/errorMessages";
import { validateEmail } from "../utils/validators";

export default function ForgotPasswordScreen({ navigation }) {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [linkLoading, setLinkLoading] = useState(false);

  async function handleReset() {
    const validation = validateEmail(email);
    if (validation) {
      setError(validation);
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");
    try {
      await sendPasswordReset(email);
      setMessage("Password reset email sent.");
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Password reset failed"));
    } finally {
      setLoading(false);
    }
  }

  async function handlePasswordless() {
    const validation = validateEmail(email);
    if (validation) {
      setError(validation);
      return;
    }
    setLinkLoading(true);
    setError("");
    setMessage("");
    try {
      await sendPasswordlessSignInLink(email);
      setMessage("Sign-in link sent. Check your email to continue.");
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Passwordless sign-in link failed"));
    } finally {
      setLinkLoading(false);
    }
  }

  return (
    <AuthScreenContainer>
      <BrandHeader
        title="Recover access"
        subtitle="Reset your password or receive a secure passwordless sign-in link."
      />
      <AppCard style={styles.form}>
        {!!error && <ErrorState message={error} />}
        {!!message && <Text style={styles.success}>{message}</Text>}
        <AppInput label="Email" value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" />
        <AppButton title="Send reset link" icon="key-outline" onPress={handleReset} loading={loading} />
        <AppButton title="Email me a sign-in link" icon="mail-outline" variant="secondary" onPress={handlePasswordless} loading={linkLoading} />
        <AppButton title="Back to login" variant="ghost" onPress={() => navigation.goBack()} />
      </AppCard>
    </AuthScreenContainer>
  );
}

const styles = StyleSheet.create({
  form: {
    gap: spacing.md
  },
  success: {
    color: colors.success,
    fontWeight: "800",
    padding: spacing.md,
    borderRadius: spacing.cardRadius,
    backgroundColor: colors.successSurface
  }
});
