import { SafeAreaView } from "react-native-safe-area-context";
import { Platform, ScrollView, StyleSheet, View } from "react-native";
import { StatusBar } from "expo-status-bar";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

export default function Screen({ children, scroll = true, padded = true, refreshControl, contentStyle }) {
  const content = <View style={[styles.content, Platform.OS === "web" && styles.webContent, padded && styles.padded, contentStyle]}>{children}</View>;

  return (
    <SafeAreaView style={[styles.safeArea, Platform.OS === "web" && styles.webSafeArea]}>
      <StatusBar style="light" />
      {scroll ? (
        <ScrollView
          style={styles.scroller}
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
          refreshControl={refreshControl}
        >
          {content}
        </ScrollView>
      ) : content}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    minHeight: "100%",
    backgroundColor: colors.background
  },
  webSafeArea: {
    minHeight: "100vh"
  },
  scroller: {
    flex: 1,
    backgroundColor: colors.background
  },
  scrollContent: {
    flexGrow: 1,
    backgroundColor: colors.background
  },
  content: {
    flex: 1,
    flexGrow: 1
  },
  webContent: {
    minHeight: "100vh"
  },
  padded: {
    padding: spacing.screen
  }
});
