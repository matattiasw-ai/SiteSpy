import { createContext, useContext } from "react";

export const AuthContext = createContext({
  user: null,
  setUser: () => {},
  localContext: null,
  refreshLocalContext: async () => {}
});

export function useAuth() {
  return useContext(AuthContext);
}
