import { Image, StyleSheet, Text, View } from "react-native";
import LoadingState from "../components/LoadingState";
import Screen from "../components/Screen";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

const stageMessages = {
  initializing: "Starting secure workspace",
  restoringAuth: "Restoring session",
  restoringLocalState: "Restoring local drafts",
  syncing: "Syncing workspace",
  failed: "Startup needs attention",
  ready: "Preparing workspace"
};

export default function SplashScreen({ startupStage = "initializing" }) {
  return (
    <Screen scroll={false}>
      <View style={styles.wrap}>
        <Image source={require("../../assets/logo-mark-transparent.png")} style={styles.logo} resizeMode="contain" />
        <Text style={styles.title}>SiteSpy</Text>
        <Text style={styles.subtitle}>Wall material and labour estimation</Text>
        <LoadingState message={stageMessages[startupStage] || "Preparing workspace"} />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  wrap: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: spacing.xl,
    backgroundColor: colors.background
  },
  logo: {
    width: 112,
    height: 112
  },
  title: {
    marginTop: spacing.lg,
    color: colors.text,
    fontWeight: "900",
    fontSize: 30
  },
  subtitle: {
    marginTop: spacing.sm,
    color: colors.muted,
    textAlign: "center"
  }
});
