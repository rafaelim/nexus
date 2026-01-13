import { Show } from 'solid-js';
import { A, useLocation } from '@solidjs/router';

const SettingsSidePanel = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  // Determine which domain's sections to show based on route
  const isFinanceRoute = () => {
    return location.pathname.startsWith('/settings/finance');
  };

  // Get the current section name based on route
  const getCurrentSection = () => {
    if (isFinanceRoute()) {
      return 'Finance';
    }
    return 'Settings';
  };

  return (
    <Show when={location.pathname.startsWith('/settings')}>
      <div class="bg-gray-50 w-64 h-screen fixed right-0 top-0 z-30 relative">
        {/* Faded left border */}
        <div 
          class="absolute left-0 top-0 bottom-0 w-px"
          style={{
            'background': 'linear-gradient(to bottom, transparent 0%, rgb(229, 231, 235) 10%, rgb(229, 231, 235) 90%, transparent 100%)'
          }}
        />
        <div class="flex flex-col h-full">
          {/* Header */}
          <div class="p-8 pb-4">
            <h2 class="text-lg font-semibold text-gray-900">{getCurrentSection()}</h2>
          </div>

          {/* Navigation */}
          <nav class="flex-1 overflow-y-auto p-4">
            <Show when={isFinanceRoute()}>
              <div class="space-y-1">
                <A
                  href="/settings/finance/categories"
                  class={`block px-3 py-2 text-sm rounded-md transition-colors ${
                    isActive('/settings/finance/categories')
                      ? 'bg-indigo-100 text-indigo-700 font-medium'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  Categories
                </A>
              </div>
            </Show>
          </nav>
        </div>
      </div>
    </Show>
  );
};

export default SettingsSidePanel;

