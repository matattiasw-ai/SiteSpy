import { useState } from "react";
import { StyleSheet, Text, View } from "react-native";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import AppInput from "../components/AppInput";
import AuthScreenContainer from "../components/AuthScreenContainer";
import BrandHeader from "../components/BrandHeader";
import ErrorState from "../components/ErrorState";
import { loginWithEmail, sendPasswordlessSignInLink } from "../services/authService";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { logAndGetUserMessage } from "../utils/errorMessages";
import { collectErrors, requireText, validateEmail } from "../utils/validators";

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [passwordlessLoading, setPasswordlessLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function handleLogin() {
    const errors = collectErrors([
      () => validateEmail(email),
      () => requireText(password, "Password")
    ]);
    if (errors.length) {
      setError(errors[0]);
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");
    try {
      await loginWithEmail(email, password);
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Login failed"));
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
    setPasswordlessLoading(true);
    setError("");
    setMessage("");
    try {
      await sendPasswordlessSignInLink(email);
      setMessage("Sign-in link sent. Check your email to continue.");
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Passwordless sign-in link failed"));
    } finally {
      setPasswordlessLoading(false);
    }
  }

  return (
    <AuthScreenContainer>
      <BrandHeader
        title="Secure field estimates"
        subtitle="Manage projects, calculations, images, and cost history from your Android workspace."
      />
      <AppCard style={styles.form}>
        <Text style={styles.formTitle}>Welcome back</Text>
        {!!error && <ErrorState message={error} />}
        {!!message && <Text style={styles.success}>{message}</Text>}
        <AppInput label="Email" value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" />
        <AppInput label="Password" value={password} onChangeText={setPassword} secureTextEntry />
        <AppButton title="Log in" icon="lock-closed-outline" onPress={handleLogin} loading={loading} />
        <AppButton title="Email me a sign-in link" icon="mail-outline" variant="secondary" onPress={handlePasswordless} loading={passwordlessLoading} />
        <View style={styles.links}>
          <AppButton title="Create account" variant="ghost" onPress={() => navigation.navigate("Register")} />
          <AppButton title="Forgot password" variant="ghost" onPress={() => navigation.navigate("ForgotPassword")} />
        </View>
      </AppCard>
      <Text style={styles.footer}>SiteSpy keeps each project linked to your account.</Text>
    </AuthScreenContainer>
  );
}

const styles = StyleSheet.create({
  form: {
    gap: spacing.md
  },
  formTitle: {
    color: colors.text,
    fontWeight: "900",
    fontSize: 21
  },
  links: {
    gap: spacing.sm,
    marginTop: spacing.xs
  },
  success: {
    color: colors.success,
    fontWeight: "800",
    padding: spacing.md,
    borderRadius: spacing.cardRadius,
    backgroundColor: colors.successSurface
  },
  footer: {
    marginTop: spacing.lg,
    color: colors.mutedSoft,
    textAlign: "center",
    lineHeight: 20
  }
});
