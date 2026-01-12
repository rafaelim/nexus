import { createSignal } from 'solid-js';

export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

const [user, setUser] = createSignal<User | null>(null);
const [isAuthenticated, setIsAuthenticated] = createSignal<boolean>(false);

// Check if user is authenticated on load
const token = localStorage.getItem('access_token');
if (token) {
  setIsAuthenticated(true);
}

export const useAuthStore = () => {
  const login = (userData: User, token: string) => {
    localStorage.setItem('access_token', token);
    setUser(userData);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    setIsAuthenticated(false);
  };

  const setUserData = (userData: User) => {
    setUser(userData);
  };

  return {
    user,
    isAuthenticated,
    login,
    logout,
    setUserData,
  };
};

