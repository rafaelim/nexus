import { A } from '@solidjs/router';

const Navigation = () => {
  return (
    <nav class="bg-white shadow-sm border-b">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-8">
            <A href="/" class="text-xl font-bold text-gray-900">
              Nexus
            </A>
            <div class="flex space-x-4">
              <A href="/dashboard" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                Dashboard
              </A>
              <A href="/transactions" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                Transactions
              </A>
              <A href="/categories" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                Categories
              </A>
              <A href="/recurring-expenses" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                Recurring Expenses
              </A>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;

