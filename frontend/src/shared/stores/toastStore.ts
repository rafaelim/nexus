import { createSignal } from 'solid-js';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface Toast {
  id: string;
  message: string;
  type: ToastType;
  duration?: number;
}

const [toasts, setToasts] = createSignal<Toast[]>([]);

export const toastStore = {
  toasts,
  
  add: (message: string, type: ToastType = 'info', duration: number = 3000) => {
    const id = Math.random().toString(36).substring(2, 9);
    const toast: Toast = { id, message, type, duration };
    
    setToasts([...toasts(), toast]);
    
    if (duration > 0) {
      setTimeout(() => {
        toastStore.remove(id);
      }, duration);
    }
    
    return id;
  },
  
  remove: (id: string) => {
    setToasts(toasts().filter(t => t.id !== id));
  },
  
  success: (message: string, duration?: number) => {
    return toastStore.add(message, 'success', duration);
  },
  
  error: (message: string, duration?: number) => {
    return toastStore.add(message, 'error', duration || 5000);
  },
  
  info: (message: string, duration?: number) => {
    return toastStore.add(message, 'info', duration);
  },
  
  warning: (message: string, duration?: number) => {
    return toastStore.add(message, 'warning', duration);
  },
  
  clear: () => {
    setToasts([]);
  },
};

