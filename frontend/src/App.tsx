import { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { SummarizeForm } from "./components/SummarizeForm";
import { SummaryDisplay } from "./components/SummaryDisplay";
import { ErrorBanner } from "./components/ErrorBanner";
import { Header } from "./components/Header";
import { ThemeProvider } from "./ThemeContext";
import { LoginForm } from "./components/LoginForm";
import { HistoryDisplay } from "./components/HistoryDisplay";
import { AuthProvider } from "./AuthContext";
import { ProtectedRoute, PublicOnlyRoute } from "./components/ProtectedRoute";
import type { ApiError, SummarizeResponse } from "./types";

import "./App.css";

/**
 * Home page with summarize form (protected)
 */
function HomePage() {
  const [result, setResult] = useState<SummarizeResponse | null>(null);
  const [error, setError] = useState<ApiError | null>(null);

  return (
    <>
      <Header />
      <main className="app">
        <HistoryDisplay />

        <SummarizeForm onResult={setResult} onError={setError} />
        <ErrorBanner error={error} />
        <SummaryDisplay result={result} />
      </main>
    </>
  );
}

/**
 * Login page (public only - redirect if already logged in)
 */
function LoginPage() {
  return (
    <div className="auth-page">
      <div className="auth-container">
        <LoginForm />
      </div>
    </div>
  );
}

/**
 * Main app with routing
 */
function AppContent() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={
            <PublicOnlyRoute>
              <LoginPage />
            </PublicOnlyRoute>
          }
        />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ThemeProvider>
  );
}
