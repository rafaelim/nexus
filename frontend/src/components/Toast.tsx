import { For, Show } from 'solid-js';
import { toastStore, type ToastType } from '../shared/stores/toastStore';

const Toast = () => {
  const getToastStyles = (type: ToastType) => {
    const baseStyles = 'px-4 py-3 rounded-lg shadow-lg flex items-center justify-between min-w-[300px] max-w-md';
    const typeStyles = {
      success: 'bg-green-500 text-white',
      error: 'bg-red-500 text-white',
      info: 'bg-blue-500 text-white',
      warning: 'bg-yellow-500 text-white',
    };
    return `${baseStyles} ${typeStyles[type]}`;
  };

  const getIcon = (type: ToastType) => {
    switch (type) {
      case 'success':
        return (
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        );
      case 'error':
        return (
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        );
      case 'warning':
        return (
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        );
      default:
        return (
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
    }
  };

  return (
    <div class="fixed top-4 right-4 z-50 space-y-2">
      <For each={toastStore.toasts()}>
        {(toast) => (
          <div
            class={`${getToastStyles(toast.type)} animate-slide-in`}
            style="animation: slideIn 0.3s ease-out;"
          >
            <div class="flex items-center space-x-3">
              {getIcon(toast.type)}
              <p class="text-sm font-medium">{toast.message}</p>
            </div>
            <button
              onClick={() => toastStore.remove(toast.id)}
              class="ml-4 text-white hover:text-gray-200"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        )}
      </For>
    </div>
  );
};

export default Toast;

