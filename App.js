import { useMemo } from "react";
import { StyleSheet, Text, View } from "react-native";

export default function App() {
  const root = useMemo(() => {
    try {
      return { RootApp: require("./src/App").default, error: null };
    } catch (error) {
      console.error("[SiteSpy] Root startup import failed", error);
      return { RootApp: null, error };
    }
  }, []);

  if (root.error || !root.RootApp) {
    return (
      <View style={styles.wrap}>
        <Text style={styles.title}>SiteSpy startup error</Text>
        <Text style={styles.message}>{root.error?.message || "Unknown startup error"}</Text>
      </View>
    );
  }

  const RootApp = root.RootApp;
  return <RootApp />;
}

const styles = StyleSheet.create({
  wrap: {
    flex: 1,
    justifyContent: "center",
    padding: 24,
    backgroundColor: "#07101E"
  },
  title: {
    color: "#F8FBFF",
    fontSize: 24,
    fontWeight: "900",
    marginBottom: 12
  },
  message: {
    color: "#A8B6CC",
    lineHeight: 22
  }
});
