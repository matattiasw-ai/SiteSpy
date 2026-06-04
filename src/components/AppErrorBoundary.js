import { Component } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { buildInfo } from "../services/runtimeConfig";
import { toUserMessage } from "../utils/errorMessages";

export default class AppErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    console.error("[SiteSpy] Render error", error);
    console.error("[SiteSpy] Component stack", info?.componentStack);
  }

  render() {
    if (!this.state.error) {
      return this.props.children;
    }

    const showDebugMessage =
      (typeof __DEV__ !== "undefined" && __DEV__) ||
      buildInfo.appEnvironment !== "production";
    const message = showDebugMessage
      ? this.state.error?.message || String(this.state.error)
      : toUserMessage(this.state.error);

    return (
      <View style={styles.wrap}>
        <Text style={styles.title}>SiteSpy could not render</Text>
        <Text style={styles.message}>{message}</Text>
        <Pressable style={styles.button} onPress={() => this.setState({ error: null })}>
          <Text style={styles.buttonText}>Try again</Text>
        </Pressable>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  wrap: {
    flex: 1,
    minHeight: "100%",
    justifyContent: "center",
    padding: 24,
    backgroundColor: "#08111F"
  },
  title: {
    color: "#F8FBFF",
    fontSize: 24,
    fontWeight: "900",
    marginBottom: 12
  },
  message: {
    color: "#A8B6CC",
    lineHeight: 22,
    marginBottom: 18
  },
  button: {
    alignSelf: "flex-start",
    borderRadius: 10,
    paddingHorizontal: 18,
    paddingVertical: 12,
    backgroundColor: "#25C7F7"
  },
  buttonText: {
    color: "#08111F",
    fontWeight: "900"
  }
});
