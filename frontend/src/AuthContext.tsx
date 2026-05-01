import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { isAuthenticated as checkAuth, getStoredToken, removeStoredToken } from "./api";

interface AuthContextType {
  isAuthenticated: boolean;
  login: () => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    setAuthenticated(checkAuth());
  }, []);

  const login = () => {
    setAuthenticated(true);
  };

  const logout = () => {
    removeStoredToken();
    setAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated: authenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to access auth context.
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}