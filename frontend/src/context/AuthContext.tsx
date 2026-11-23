import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { UserProfile } from '../types';

interface AuthContextType {
  user: UserProfile | null;
  isLoggedIn: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, email: string) => Promise<void>;
  logout: () => void;
  authError: string | null;
  setAuthError: (err: string | null) => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoggedIn: false,
  login: async () => {},
  register: async () => {},
  logout: () => {},
  authError: null,
  setAuthError: () => {}
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(() => {
    try {
      const saved = localStorage.getItem('polygen_auth') || localStorage.getItem('polygen_user');
      return saved ? JSON.parse(saved) : null; // Strictly NULL if not authenticated!
    } catch {
      return null;
    }
  });

  const [authError, setAuthError] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      localStorage.setItem('polygen_auth', JSON.stringify(user));
      localStorage.setItem('polygen_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('polygen_auth');
      localStorage.removeItem('polygen_user');
    }
  }, [user]);

  const login = async (username: string, password: string) => {
    setAuthError(null);
    try {
      const res = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (!res.ok) {
        throw new Error('Wrong credentials');
      }

      const data = await res.json();
      const profile: UserProfile = {
        name: data.user.display_name || data.user.username,
        email: data.user.email || `${username}@polygen.ai`,
        role: data.user.role || 'Studio Lead',
        plan: 'Enterprise Pro',
        avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=256&q=80'
      };

      setUser(profile);
    } catch (err: any) {
      setAuthError('Wrong credentials');
      throw err;
    }
  };

  const register = async (username: string, password: string, email: string) => {
    setAuthError(null);
    try {
      const res = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, email })
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Registration failed');
      }

      const data = await res.json();
      const profile: UserProfile = {
        name: data.user.display_name || data.user.username,
        email: data.user.email || email,
        role: data.user.role || 'Studio Developer',
        plan: 'Developer Tier',
        avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=256&q=80'
      };

      setUser(profile);
    } catch (err: any) {
      setAuthError(err.message || 'Registration failed');
      throw err;
    }
  };

  const logout = () => {
    setUser(null);
    setAuthError(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoggedIn: !!user,
        login,
        register,
        logout,
        authError,
        setAuthError
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
