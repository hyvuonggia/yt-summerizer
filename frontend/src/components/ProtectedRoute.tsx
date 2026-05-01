/**
 * Protected Route component.
 * 
 * Redirects unauthenticated users to login page.
 */

import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../AuthContext";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

/**
 * Route that requires authentication.
 * If not authenticated, redirects to /login with return URL.
 */
export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const auth = useAuth();
  const location = useLocation();

  if (!auth.isAuthenticated) {
    // Redirect to login, remembering where user came from
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}

/**
 * Route that redirects to home if already authenticated.
 * Useful for /login, /register pages.
 */
export function PublicOnlyRoute({ children }: ProtectedRouteProps) {
  const auth = useAuth();

  if (auth.isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}