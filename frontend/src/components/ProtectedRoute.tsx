import { Show } from 'solid-js';
import { Navigate } from '@solidjs/router';
import { useAuthStore } from '../shared/stores/authStore';

interface ProtectedRouteProps {
  children: JSX.Element;
}

const ProtectedRoute = (props: ProtectedRouteProps) => {
  const { isAuthenticated } = useAuthStore();

  return (
    <Show when={isAuthenticated()} fallback={<Navigate href="/login" />}>
      {props.children}
    </Show>
  );
};

export default ProtectedRoute;

