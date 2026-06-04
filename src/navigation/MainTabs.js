import { Ionicons } from "@expo/vector-icons";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import DashboardScreen from "../screens/DashboardScreen";
import EditProjectScreen from "../screens/EditProjectScreen";
import EstimateSummaryScreen from "../screens/EstimateSummaryScreen";
import ImageEstimateScreen from "../screens/ImageEstimateScreen";
import ManualEstimateScreen from "../screens/ManualEstimateScreen";
import NewProjectScreen from "../screens/NewProjectScreen";
import ProfileScreen from "../screens/ProfileScreen";
import ProjectDetailsScreen from "../screens/ProjectDetailsScreen";
import ProjectHistoryScreen from "../screens/ProjectHistoryScreen";
import SettingsScreen from "../screens/SettingsScreen";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";

const stackScreenOptions = {
  headerStyle: { backgroundColor: colors.backgroundAlt },
  headerTintColor: colors.text,
  headerTitleStyle: { fontWeight: "900" },
  headerShadowVisible: false,
  contentStyle: { backgroundColor: colors.background }
};

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

function ProjectStack() {
  return (
    <Stack.Navigator
      screenOptions={stackScreenOptions}
    >
      <Stack.Screen name="ProjectHistory" component={ProjectHistoryScreen} options={{ title: "Project History" }} />
      <Stack.Screen name="ProjectDetails" component={ProjectDetailsScreen} options={{ title: "Project Details" }} />
      <Stack.Screen name="EditProject" component={EditProjectScreen} options={{ title: "Edit Project" }} />
      <Stack.Screen name="ManualEstimate" component={ManualEstimateScreen} options={{ title: "Manual Estimate" }} />
      <Stack.Screen name="ImageEstimate" component={ImageEstimateScreen} options={{ title: "Image Estimate" }} />
      <Stack.Screen name="EstimateSummary" component={EstimateSummaryScreen} options={{ title: "Estimate Summary" }} />
    </Stack.Navigator>
  );
}

function CreateStack() {
  return (
    <Stack.Navigator
      screenOptions={stackScreenOptions}
    >
      <Stack.Screen name="NewProject" component={NewProjectScreen} options={{ title: "New Project" }} />
      <Stack.Screen name="ManualEstimate" component={ManualEstimateScreen} options={{ title: "Manual Estimate" }} />
      <Stack.Screen name="ImageEstimate" component={ImageEstimateScreen} options={{ title: "Image Estimate" }} />
      <Stack.Screen name="EstimateSummary" component={EstimateSummaryScreen} options={{ title: "Estimate Summary" }} />
      <Stack.Screen name="ProjectDetails" component={ProjectDetailsScreen} options={{ title: "Project Details" }} />
      <Stack.Screen name="EditProject" component={EditProjectScreen} options={{ title: "Edit Project" }} />
    </Stack.Navigator>
  );
}

function ProfileStack() {
  return (
    <Stack.Navigator
      screenOptions={stackScreenOptions}
    >
      <Stack.Screen name="Profile" component={ProfileScreen} />
      <Stack.Screen name="Settings" component={SettingsScreen} />
    </Stack.Navigator>
  );
}

const icons = {
  Dashboard: "grid-outline",
  Projects: "folder-open-outline",
  New: "add-circle-outline",
  ProfileTab: "person-circle-outline"
};

export default function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.muted,
        tabBarStyle: {
          backgroundColor: colors.backgroundAlt,
          borderTopColor: colors.borderSoft,
          height: 68,
          paddingTop: spacing.xs,
          paddingBottom: spacing.sm
        },
        tabBarLabelStyle: {
          fontWeight: "800"
        },
        tabBarIcon: ({ color, size, focused }) => <Ionicons name={icons[route.name]} size={focused ? size + 2 : size} color={color} />
      })}
    >
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Projects" component={ProjectStack} />
      <Tab.Screen name="New" component={CreateStack} options={{ title: "New" }} />
      <Tab.Screen name="ProfileTab" component={ProfileStack} options={{ title: "Profile" }} />
    </Tab.Navigator>
  );
}
