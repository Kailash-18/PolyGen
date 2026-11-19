import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { UserProfile } from '../types';

interface AuthContextType {
  user: UserProfile | null;
  isLoggedIn: boolean;
  showAuthModal: boolean;
  setShowAuthModal: (open: boolean) => void;
  login: (email?: string, password?: string) => Promise<void>;
  logout: () => void;
}

const DEFAULT_USER: UserProfile = {
  name: 'Kailash',
  email: 'kailash@polygen.ai',
  role: 'Frontend & 3D Lead',
  plan: 'Pro Studio',
  avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=256&q=80'
};

const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoggedIn: false,
  showAuthModal: false,
  setShowAuthModal: () => {},
  login: async () => {},
  logout: () => {}
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(() => {
    const saved = localStorage.getItem('polygen_user');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return DEFAULT_USER;
      }
    }
    return DEFAULT_USER;
  });

  const [showAuthModal, setShowAuthModal] = useState(false);

  useEffect(() => {
    if (user) {
      localStorage.setItem('polygen_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('polygen_user');
    }
  }, [user]);

  const login = async (email: string = 'kailash@polygen.ai') => {
    try {
      const res = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data.user);
      } else {
        setUser({ ...DEFAULT_USER, email });
      }
    } catch {
      setUser({ ...DEFAULT_USER, email });
    }
    setShowAuthModal(false);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoggedIn: !!user,
        showAuthModal,
        setShowAuthModal,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
