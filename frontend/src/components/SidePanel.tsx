import { createSignal, Show, createEffect } from 'solid-js';
import { A, useLocation } from '@solidjs/router';

const SidePanel = () => {
  const [isCollapsed, setIsCollapsed] = createSignal(false);
  const [expandedDomains, setExpandedDomains] = createSignal<Set<string>>(new Set(['expenses']));
  const location = useLocation();

  // Auto-expand Settings if on settings route
  createEffect(() => {
    if (location.pathname.startsWith('/settings') && !expandedDomains().has('settings')) {
      setExpandedDomains(new Set([...expandedDomains(), 'settings']));
    }
  });

  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed());
  };

  const toggleDomain = (domain: string) => {
    const current = expandedDomains();
    const newSet = new Set(current);
    if (newSet.has(domain)) {
      newSet.delete(domain);
    } else {
      newSet.add(domain);
    }
    setExpandedDomains(newSet);
  };

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <div
      class={`bg-white border-r border-gray-200 transition-all duration-300 ${
        isCollapsed() ? 'w-16' : 'w-64'
      } h-[calc(100vh-4rem)] fixed left-0 top-16 z-40`}
    >
      <div class="flex flex-col h-full">
        {/* Navigation */}
        <nav class="flex-1 overflow-y-auto p-4">
          <Show when={!isCollapsed()}>
            {/* Expenses Domain */}
            <div class="mb-4">
              <div class="w-full flex items-center justify-between px-3 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-100 rounded-md transition-colors">
                <A
                  href="/expenses"
                  class="flex-1 text-left"
                >
                  Expenses
                </A>
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    toggleDomain('expenses');
                  }}
                  class="p-1 hover:bg-gray-200 rounded ml-2"
                  title="Toggle menu"
                >
                  <svg
                    class={`w-4 h-4 transition-transform ${
                      expandedDomains().has('expenses') ? 'rotate-90' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </button>
              </div>
              <Show when={expandedDomains().has('expenses')}>
                <div class="ml-4 mt-1 space-y-1">
                  <A
                    href="/expenses"
                    class={`block px-3 py-2 text-sm rounded-md transition-colors ${
                      isActive('/expenses')
                        ? 'bg-indigo-100 text-indigo-700 font-medium'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    Dashboard
                  </A>
                  <A
                    href="/expenses/transactions"
                    class={`block px-3 py-2 text-sm rounded-md transition-colors ${
                      isActive('/expenses/transactions')
                        ? 'bg-indigo-100 text-indigo-700 font-medium'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    Transactions
                  </A>
                  <A
                    href="/expenses/expenses"
                    class={`block px-3 py-2 text-sm rounded-md transition-colors ${
                      isActive('/expenses/expenses')
                        ? 'bg-indigo-100 text-indigo-700 font-medium'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    Expenses
                  </A>
                  <A
                    href="/expenses/monthly-notes"
                    class={`block px-3 py-2 text-sm rounded-md transition-colors ${
                      isActive('/expenses/monthly-notes')
                        ? 'bg-indigo-100 text-indigo-700 font-medium'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    Monthly Notes
                  </A>
                </div>
              </Show>
            </div>

            {/* Settings Domain */}
            <div class="mb-4">
              <div class="w-full flex items-center justify-between px-3 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-100 rounded-md transition-colors">
                <A
                  href="/settings/general"
                  class="flex-1 text-left"
                >
                  Settings
                </A>
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    toggleDomain('settings');
                  }}
                  class="p-1 hover:bg-gray-200 rounded ml-2"
                  title="Toggle menu"
                >
                  <svg
                    class={`w-4 h-4 transition-transform ${
                      expandedDomains().has('settings') ? 'rotate-90' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </button>
              </div>
              <Show when={expandedDomains().has('settings')}>
                <div class="ml-4 mt-1 space-y-1">
                  <A
                    href="/settings/general"
                    class={`block px-3 py-2 text-sm rounded-md transition-colors ${
                      isActive('/settings/general') || isActive('/settings/general/houses')
                        ? 'bg-indigo-100 text-indigo-700 font-medium'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    General
                  </A>
                  <A
                    href="/settings/finance"
                    class={`block px-3 py-2 text-sm rounded-md transition-colors ${
                      isActive('/settings/finance') || isActive('/settings/finance/categories')
                        ? 'bg-indigo-100 text-indigo-700 font-medium'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    Finance
                  </A>
                </div>
              </Show>
            </div>
          </Show>

          {/* Collapsed view - show icons only */}
          <Show when={isCollapsed()}>
            <div class="space-y-2">
              <A
                href="/expenses"
                class="block p-3 text-gray-600 hover:bg-gray-100 rounded-md transition-colors"
                title="Expenses"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </A>
              <A
                href="/settings/general"
                class="block p-3 text-gray-600 hover:bg-gray-100 rounded-md transition-colors"
                title="Settings"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                </svg>
              </A>
            </div>
          </Show>
        </nav>

        {/* Footer with collapse button */}
        <div class="border-t border-gray-200 p-2">
          <button
            onClick={toggleCollapse}
            class="w-full p-1.5 rounded-md hover:bg-gray-100 text-gray-500 flex items-center justify-center transition-colors"
            title={isCollapsed() ? 'Expand' : 'Collapse'}
          >
            <svg
              class={`w-4 h-4 transition-transform ${isCollapsed() ? '' : 'rotate-180'}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default SidePanel;

