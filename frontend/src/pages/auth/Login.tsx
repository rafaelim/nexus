import { createSignal } from 'solid-js';
import { useNavigate, A } from '@solidjs/router';
import { authService } from '../../services/auth/authService';
import { useAuthStore } from '../../shared/stores/authStore';
import AuthForm from './components/AuthForm';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuthStore();
  const [error, setError] = createSignal<string>('');

  const handleSubmit = async (email: string, password: string) => {
    try {
      setError('');
      const response = await authService.login({ email, password });
      login(response.user, response.access_token);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
        </div>
        <AuthForm
          onSubmit={handleSubmit}
          error={error()}
          isLogin={true}
        />
        <p class="mt-2 text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <A href="/register" class="font-medium text-indigo-600 hover:text-indigo-500">
            Sign up
          </A>
        </p>
      </div>
    </div>
  );
};

export default Login;

