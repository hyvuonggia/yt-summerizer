import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { loginUser, registerUser } from "../api";
import { useAuth } from "../AuthContext";

interface LoginFormProps {
  onLoginSuccess?: () => void;
}

/**
 * Login/Signup form component.
 */
export function LoginForm({ onLoginSuccess }: LoginFormProps) {
  const [isLoginView, setIsLoginView] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: Location })?.from?.pathname || "/";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isLoginView) {
        await loginUser(email, password);
      } else {
        await registerUser(email, password, username || undefined);
      }
      // Update auth context state
      login();
      onLoginSuccess?.();
      // Redirect to home
      navigate(from, { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <h2>{isLoginView ? "Login" : "Sign Up"}</h2>
      
      <form onSubmit={handleSubmit} className="login-form">
        {!isLoginView && (
          <div className="form-group">
            <label htmlFor="username">Username (optional)</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Your username"
            />
          </div>
        )}
        
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="you@example.com"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            placeholder="Minimum 8 characters"
          />
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Loading..." : isLoginView ? "Login" : "Sign Up"}
        </button>
      </form>
      
      <p className="login-toggle">
        {isLoginView ? "Don't have an account? " : "Already have an account? "}
        <button
          type="button"
          onClick={() => {
            setIsLoginView(!isLoginView);
            setError("");
          }}
          className="btn-link"
        >
          {isLoginView ? "Sign Up" : "Login"}
        </button>
      </p>
    </div>
  );
}