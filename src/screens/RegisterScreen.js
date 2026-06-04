import { useState } from "react";
import { StyleSheet, Text } from "react-native";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import AppInput from "../components/AppInput";
import AuthScreenContainer from "../components/AuthScreenContainer";
import BrandHeader from "../components/BrandHeader";
import ErrorState from "../components/ErrorState";
import { registerWithEmail } from "../services/authService";
import { spacing } from "../theme/spacing";
import { logAndGetUserMessage } from "../utils/errorMessages";
import { collectErrors, requireText, validateEmail } from "../utils/validators";

export default function RegisterScreen({ navigation }) {
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleRegister() {
    const errors = collectErrors([
      () => validateEmail(email),
      () => requireText(password, "Password"),
      () => (password.length < 6 ? "Password must be at least 6 characters." : ""),
      () => (password !== confirmPassword ? "Passwords must match." : "")
    ]);
    if (errors.length) {
      setError(errors[0]);
      return;
    }

    setLoading(true);
    setError("");
    try {
      await registerWithEmail(email, password, { displayName });
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Registration failed"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthScreenContainer>
      <BrandHeader
        title="Create account"
        subtitle="Create a secure profile for project history and saved estimates."
      />
      <AppCard style={styles.form}>
        {!!error && <ErrorState message={error} />}
        <AppInput label="Full name (optional)" value={displayName} onChangeText={setDisplayName} autoCapitalize="words" />
        <AppInput label="Email" value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" />
        <AppInput label="Password" value={password} onChangeText={setPassword} secureTextEntry helperText="Use at least 6 characters." />
        <AppInput label="Confirm password" value={confirmPassword} onChangeText={setConfirmPassword} secureTextEntry />
        <AppButton title="Create account" icon="person-add-outline" onPress={handleRegister} loading={loading} />
        <AppButton title="Back to login" variant="ghost" onPress={() => navigation.goBack()} />
      </AppCard>
    </AuthScreenContainer>
  );
}

const styles = StyleSheet.create({
  form: {
    gap: spacing.md
  }
});
