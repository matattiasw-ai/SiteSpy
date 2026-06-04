import { NavigationContainer } from "@react-navigation/native";
import { useEffect, useMemo, useState } from "react";
import { Platform, StyleSheet } from "react-native";
import { SafeAreaProvider } from "react-native-safe-area-context";
import AppErrorBoundary from "./components/AppErrorBoundary";
import RuntimeConfigDiagnosticScreen from "./components/RuntimeConfigDiagnosticScreen";
import { AuthContext } from "./services/authContext";
import { completePasswordlessFromCurrentUrl, subscribeToAuthState } from "./services/authService";
import { restoreLocalContext } from "./services/localStateService";
import { logStartupDiagnostics, shouldShowRuntimeConfigDiagnostic } from "./services/runtimeConfig";
import { toUserMessage } from "./utils/errorMessages";
import AppNavigator from "./navigation/AppNavigator";

logStartupDiagnostics();

export default function App() {
  const [initializing, setInitializing] = useState(true);
  const [startupStage, setStartupStage] = useState("initializing");
  const [user, setUser] = useState(null);
  const [localContext, setLocalContext] = useState(null);

  async function refreshLocalContext(nextUser = user) {
    if (!nextUser?.uid) {
      setLocalContext(null);
      return null;
    }
    setStartupStage("restoringLocalState");
    const restored = await restoreLocalContext(nextUser.uid);
    setLocalContext(restored);
    setStartupStage("ready");
    return restored;
  }

  useEffect(() => {
    const canUseWindowEvents =
      typeof window !== "undefined" &&
      typeof window.addEventListener === "function" &&
      typeof window.removeEventListener === "function";
    console.log("[SiteSpy] before window.addEventListener", typeof window !== "undefined" ? typeof window.addEventListener : "undefined");

    if (canUseWindowEvents) {
      const handleError = (event) => {
        console.error("[SiteSpy] Window error", event.error || event.message);
      };
      const handleRejection = (event) => {
        console.error("[SiteSpy] Unhandled promise rejection", event.reason);
      };
      window.addEventListener("error", handleError);
      window.addEventListener("unhandledrejection", handleRejection);
      return () => {
        console.log("[SiteSpy] before window.removeEventListener", typeof window.removeEventListener);
        if (typeof window.removeEventListener === "function") {
          window.removeEventListener("error", handleError);
          window.removeEventListener("unhandledrejection", handleRejection);
        }
      };
    }
    return undefined;
  }, []);

  useEffect(() => {
    console.log("[SiteSpy] before auth startup effect", {
      shouldShowRuntimeConfigDiagnostic,
      subscribeToAuthState: typeof subscribeToAuthState
    });
    if (shouldShowRuntimeConfigDiagnostic) {
      setInitializing(false);
      return () => {};
    }
    try {
      if (typeof subscribeToAuthState !== "function") {
        console.error("[SiteSpy] subscribeToAuthState is not callable", typeof subscribeToAuthState);
        setInitializing(false);
        return () => {};
      }
      console.log("[SiteSpy] before subscribeToAuthState", typeof subscribeToAuthState);
      const unsubscribe = subscribeToAuthState(async (nextUser) => {
        setStartupStage("restoringAuth");
        setUser(nextUser);
        if (nextUser?.uid) {
          await refreshLocalContext(nextUser);
        } else {
          setLocalContext(null);
          setStartupStage("ready");
        }
        setInitializing(false);
      });
      return () => {
        console.log("[SiteSpy] before auth unsubscribe", typeof unsubscribe);
        if (typeof unsubscribe === "function") {
          unsubscribe();
        }
      };
    } catch (error) {
      console.error("[SiteSpy] Auth subscription failed", error);
      setStartupStage("failed");
      setInitializing(false);
      return () => {};
    }
  }, []);

  useEffect(() => {
    console.log("[SiteSpy] before passwordless startup effect", {
      shouldShowRuntimeConfigDiagnostic,
      completePasswordlessFromCurrentUrl: typeof completePasswordlessFromCurrentUrl
    });
    if (shouldShowRuntimeConfigDiagnostic) {
      return;
    }
    if (typeof completePasswordlessFromCurrentUrl !== "function") {
      console.error("[SiteSpy] completePasswordlessFromCurrentUrl is not callable", typeof completePasswordlessFromCurrentUrl);
      return;
    }
    console.log("[SiteSpy] before completePasswordlessFromCurrentUrl", typeof completePasswordlessFromCurrentUrl);
    const completion = completePasswordlessFromCurrentUrl();
    if (!completion || typeof completion.then !== "function") {
      console.warn("[SiteSpy] Passwordless startup did not return a promise", typeof completion);
      return;
    }
    completion.then((nextUser) => {
        if (nextUser) {
          setUser(nextUser);
          setInitializing(false);
        }
      })
      .catch((error) => console.warn("[SiteSpy] Passwordless sign-in could not complete:", toUserMessage(error)));
  }, []);

  const authValue = useMemo(() => ({ user, setUser, localContext, refreshLocalContext }), [user, localContext]);

  return (
    <AppErrorBoundary>
      <SafeAreaProvider style={[styles.root, Platform.OS === "web" && styles.webRoot]}>
        <AuthContext.Provider value={authValue}>
          {shouldShowRuntimeConfigDiagnostic ? (
            <RuntimeConfigDiagnosticScreen />
          ) : (
            <NavigationContainer
              onReady={() => {}}
              onStateChange={() => {}}
            >
              <AppNavigator user={user} initializing={initializing} startupStage={startupStage} />
            </NavigationContainer>
          )}
        </AuthContext.Provider>
      </SafeAreaProvider>
    </AppErrorBoundary>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    minHeight: "100%"
  },
  webRoot: {
    minHeight: "100vh"
  }
});
