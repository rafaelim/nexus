import { createSignal, Show } from 'solid-js';
import { A, useLocation } from '@solidjs/router';

const SidePanel = () => {
  const [isCollapsed, setIsCollapsed] = createSignal(false);
  const [expandedDomains, setExpandedDomains] = createSignal<Set<string>>(new Set(['expenses']));
  const location = useLocation();

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
      } min-h-screen fixed left-0 top-0 z-40`}
    >
      <div class="flex flex-col h-full">
        {/* Header */}
        <div class="flex items-center justify-between p-4 border-b border-gray-200">
          <Show when={!isCollapsed()}>
            <A href="/" class="text-xl font-bold text-gray-900">
              Nexus
            </A>
          </Show>
          <button
            onClick={toggleCollapse}
            class="p-2 rounded-md hover:bg-gray-100 text-gray-600"
            title={isCollapsed() ? 'Expand' : 'Collapse'}
          >
            <svg
              class={`w-5 h-5 transition-transform ${isCollapsed() ? '' : 'rotate-180'}`}
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
                    href="/expenses/categories"
                    class={`block px-3 py-2 text-sm rounded-md transition-colors ${
                      isActive('/expenses/categories')
                        ? 'bg-indigo-100 text-indigo-700 font-medium'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    Categories
                  </A>
                  <A
                    href="/expenses/ongoing"
                    class={`block px-3 py-2 text-sm rounded-md transition-colors ${
                      isActive('/expenses/ongoing')
                        ? 'bg-indigo-100 text-indigo-700 font-medium'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    Ongoing
                  </A>
                  <A
                    href="/expenses/installments"
                    class={`block px-3 py-2 text-sm rounded-md transition-colors ${
                      isActive('/expenses/installments')
                        ? 'bg-indigo-100 text-indigo-700 font-medium'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    Installments
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
            </div>
          </Show>
        </nav>
      </div>
    </div>
  );
};

export default SidePanel;

