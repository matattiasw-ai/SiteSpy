import { Platform } from "react-native";

function makeShadow(nativeShadow, webShadow) {
  return Platform.OS === "web" ? { boxShadow: webShadow } : nativeShadow;
}

export const shadows = {
  card: makeShadow(
    {
      shadowColor: "#000",
      shadowOpacity: 0.18,
      shadowRadius: 12,
      shadowOffset: { width: 0, height: 6 },
      elevation: 3
    },
    "0 14px 32px rgba(0,0,0,0.28)"
  ),
  soft: makeShadow(
    {
      shadowColor: "#000",
      shadowOpacity: 0.1,
      shadowRadius: 8,
      shadowOffset: { width: 0, height: 4 },
      elevation: 2
    },
    "0 10px 24px rgba(0,0,0,0.18)"
  )
};
