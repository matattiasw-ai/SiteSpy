import { useEffect, useMemo, useState } from "react";
import { StyleSheet, Text, View } from "react-native";
import AppHeader from "../components/AppHeader";
import AppButton from "../components/AppButton";
import AppCard from "../components/AppCard";
import AppInput from "../components/AppInput";
import EstimateResultCard from "../components/EstimateResultCard";
import ErrorState from "../components/ErrorState";
import Screen from "../components/Screen";
import { useAuth } from "../services/authContext";
import { clearDraftEstimate, getDraftEstimate, saveDraftEstimate, setActiveProject, setLastRoute } from "../services/localStateService";
import { calculateAndSaveEstimate, previewEstimate } from "../services/estimateService";
import { colors } from "../theme/colors";
import { spacing } from "../theme/spacing";
import { UNIT_TYPES } from "../utils/constants";
import { logAndGetUserMessage } from "../utils/errorMessages";
import { collectErrors, requirePositiveNumber } from "../utils/validators";

const defaults = {
  unitType: "brick",
  wallLength: "",
  wallHeight: "",
  wallThickness: "0.2",
  unitLength: "0.215",
  unitHeight: "0.065",
  unitPrice: "",
  labourRate: "",
  mortarPrice: "115",
  mortarAllowance: "0.03"
};

export default function ManualEstimateScreen({ route, navigation }) {
  const { projectId, projectTitle } = route.params;
  const { user } = useAuth();
  const [values, setValues] = useState(defaults);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [draftRestored, setDraftRestored] = useState(false);

  const estimate = useMemo(() => {
    const required = ["wallLength", "wallHeight", "unitLength", "unitHeight", "unitPrice", "labourRate"];
    if (required.some((key) => !Number(values[key]))) return null;
    return previewEstimate(values);
  }, [values]);

  useEffect(() => {
    let mounted = true;
    async function restoreDraft() {
      await setActiveProject(user.uid, { projectId, title: projectTitle || "" });
      await setLastRoute(user.uid, { name: "ManualEstimate", projectId });
      const draft = await getDraftEstimate(user.uid, projectId);
      if (mounted && draft?.values) {
        setValues((current) => ({ ...current, ...draft.values }));
        setDraftRestored(true);
      }
    }
    restoreDraft();
    return () => {
      mounted = false;
    };
  }, [user, projectId, projectTitle]);

  useEffect(() => {
    if (!user?.uid || !projectId) return;
    saveDraftEstimate(user.uid, projectId, values);
  }, [user, projectId, values]);

  function updateValue(key, value) {
    if (key === "unitType") {
      const selected = UNIT_TYPES.find((item) => item.value === value);
      setValues((current) => ({
        ...current,
        unitType: value,
        unitLength: selected.defaultLength,
        unitHeight: selected.defaultHeight
      }));
      return;
    }
    setValues((current) => ({ ...current, [key]: value }));
  }

  async function handleSave() {
    const errors = collectErrors([
      () => requirePositiveNumber(values.wallLength, "Wall length"),
      () => requirePositiveNumber(values.wallHeight, "Wall height"),
      () => requirePositiveNumber(values.unitLength, "Unit length"),
      () => requirePositiveNumber(values.unitHeight, "Unit height"),
      () => requirePositiveNumber(values.unitPrice, "Unit price"),
      () => requirePositiveNumber(values.labourRate, "Labour rate")
    ]);
    if (errors.length) {
      setError(errors[0]);
      return;
    }

    setSaving(true);
    setError("");
    try {
      const saved = await calculateAndSaveEstimate(user.uid, projectId, values);
      await clearDraftEstimate(user.uid, projectId);
      navigation.navigate("EstimateSummary", { estimate: saved, projectId });
    } catch (nextError) {
      setError(logAndGetUserMessage(nextError, "Estimate save failed"));
    } finally {
      setSaving(false);
    }
  }

  return (
    <Screen>
      <AppHeader
        kicker="Manual estimate"
        title="Wall quantity model"
        subtitle={projectTitle || "Enter wall and cost values to calculate quantities."}
      />
      {!!error && <ErrorState message={error} />}
      {draftRestored && <Text style={styles.notice}>Unfinished estimate restored from this device.</Text>}
      <View style={styles.unitSwitch}>
        {UNIT_TYPES.map((unit) => (
          <AppButton
            key={unit.value}
            title={unit.label}
            variant={values.unitType === unit.value ? "primary" : "secondary"}
            onPress={() => updateValue("unitType", unit.value)}
            style={styles.switchButton}
          />
        ))}
      </View>
      <AppCard style={styles.form}>
        <Text style={styles.groupTitle}>Wall dimensions</Text>
        <AppInput label="Wall length (m)" value={values.wallLength} onChangeText={(text) => updateValue("wallLength", text)} keyboardType="decimal-pad" />
        <AppInput label="Wall height (m)" value={values.wallHeight} onChangeText={(text) => updateValue("wallHeight", text)} keyboardType="decimal-pad" />
        <AppInput label="Wall thickness (m)" value={values.wallThickness} onChangeText={(text) => updateValue("wallThickness", text)} keyboardType="decimal-pad" />
      </AppCard>
      <AppCard style={styles.form}>
        <Text style={styles.groupTitle}>Unit size and pricing</Text>
        <AppInput label="Unit length (m)" value={values.unitLength} onChangeText={(text) => updateValue("unitLength", text)} keyboardType="decimal-pad" />
        <AppInput label="Unit height (m)" value={values.unitHeight} onChangeText={(text) => updateValue("unitHeight", text)} keyboardType="decimal-pad" />
        <AppInput label="Unit price (N$)" value={values.unitPrice} onChangeText={(text) => updateValue("unitPrice", text)} keyboardType="decimal-pad" />
        <AppInput label="Labour rate per m2 (N$)" value={values.labourRate} onChangeText={(text) => updateValue("labourRate", text)} keyboardType="decimal-pad" />
        <AppInput label="Mortar price per m3 (N$)" value={values.mortarPrice} onChangeText={(text) => updateValue("mortarPrice", text)} keyboardType="decimal-pad" />
        <AppInput label="Mortar allowance" value={values.mortarAllowance} onChangeText={(text) => updateValue("mortarAllowance", text)} keyboardType="decimal-pad" />
      </AppCard>
      <EstimateResultCard estimate={estimate} />
      <View style={styles.actions}>
        <AppButton title="Save estimate" icon="save-outline" onPress={handleSave} loading={saving} />
        <AppButton title="Add wall image" icon="camera-outline" variant="secondary" onPress={() => navigation.navigate("ImageEstimate", { projectId })} />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  unitSwitch: {
    flexDirection: "row",
    gap: spacing.md,
    marginBottom: spacing.md
  },
  switchButton: {
    flex: 1
  },
  form: {
    gap: spacing.md,
    marginBottom: spacing.lg
  },
  groupTitle: {
    color: colors.text,
    fontWeight: "900",
    fontSize: 18
  },
  actions: {
    gap: spacing.md,
    marginTop: spacing.lg
  },
  notice: {
    color: colors.success,
    fontWeight: "800",
    padding: spacing.md,
    borderRadius: spacing.cardRadius,
    backgroundColor: colors.successSurface,
    marginBottom: spacing.md
  }
});
