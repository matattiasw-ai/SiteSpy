import SplashScreen from "../screens/SplashScreen";
import AuthNavigator from "./AuthNavigator";
import MainTabs from "./MainTabs";

export default function AppNavigator({ user, initializing, startupStage }) {
  if (initializing) {
    return <SplashScreen startupStage={startupStage} />;
  }

  return user ? <MainTabs /> : <AuthNavigator />;
}
