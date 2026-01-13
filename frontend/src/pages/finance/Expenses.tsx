import { createSignal, onMount, Show } from 'solid-js';
import Layout from '../../components/Layout';
import { expenseService } from '../../services/finance/expenseService';
import type { Expense } from '../../services/finance/expenseService';
import { categoryService } from '../../services/finance/categoryService';
import type { Category } from '../../services/finance/categoryService';
import ExpenseForm from './components/ExpenseForm';
import { toastStore } from '../../shared/stores/toastStore';

const Expenses = () => {
  const [expenses, setExpenses] = createSignal<Expense[]>([]);
  const [categories, setCategories] = createSignal<Category[]>([]);
  const [loading, setLoading] = createSignal(true);
  const [showForm, setShowForm] = createSignal(false);
  const [editingExpense, setEditingExpense] = createSignal<Expense | null>(null);
  const [filterType, setFilterType] = createSignal<string>('');
  const [filterActive, setFilterActive] = createSignal<string>('');

  onMount(async () => {
    await Promise.all([loadExpenses(), loadCategories()]);
  });

  const loadCategories = async () => {
    try {
      const data = await categoryService.getAll();
      setCategories(data);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const loadExpenses = async () => {
    try {
      setLoading(true);
      const isActive = filterActive() === '' ? undefined : filterActive() === 'active';
      let data = await expenseService.getAll(isActive);
      
      // Filter by type if specified
      if (filterType() !== '') {
        data = data.filter(exp => exp.expense_type === filterType());
      }
      
      setExpenses(data);
    } catch (error) {
      console.error('Failed to load expenses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setEditingExpense(null);
    setShowForm(true);
  };

  const handleEdit = (expense: Expense) => {
    setEditingExpense(expense);
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this expense?')) return;
    try {
      await expenseService.delete(id);
      await loadExpenses();
      toastStore.success('Expense deleted successfully');
    } catch (error) {
      console.error('Failed to delete expense:', error);
      toastStore.error('Failed to delete expense');
    }
  };

  const handleToggleActive = async (expense: Expense) => {
    try {
      await expenseService.update(expense.id, { is_active: !expense.is_active });
      await loadExpenses();
      toastStore.success(`Expense ${expense.is_active ? 'deactivated' : 'activated'} successfully`);
    } catch (error) {
      console.error('Failed to toggle expense:', error);
      toastStore.error('Failed to update expense');
    }
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingExpense(null);
  };

  const handleFormSubmit = async () => {
    await loadExpenses();
    handleFormClose();
  };

  const getCategoryName = (categoryId: string) => {
    const category = categories().find(c => c.id === categoryId);
    return category?.name || 'Unknown';
  };

  const getDefaultExpenseType = (): 'ongoing' | 'installment' | undefined => {
    if (filterType() === 'ongoing') return 'ongoing';
    if (filterType() === 'installment') return 'installment';
    return undefined;
  };

  return (
    <Layout>
      <div class="max-w-7xl mx-auto">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-3xl font-bold text-gray-900">Expenses</h1>
          <button
            onClick={handleCreate}
            class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
          >
            Add Expense
          </button>
        </div>

        <div class="bg-white p-4 rounded-lg shadow mb-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select
                value={filterType()}
                onChange={(e) => {
                  setFilterType(e.currentTarget.value);
                  loadExpenses();
                }}
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="">All Types</option>
                <option value="ongoing">Ongoing</option>
                <option value="installment">Installment</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                value={filterActive()}
                onChange={(e) => {
                  setFilterActive(e.currentTarget.value);
                  loadExpenses();
                }}
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="">All</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
          </div>
        </div>

        <Show when={showForm()}>
          <ExpenseForm
            expense={editingExpense()}
            categories={categories()}
            onClose={handleFormClose}
            onSubmit={handleFormSubmit}
            defaultExpenseType={getDefaultExpenseType()}
          />
        </Show>

        <Show when={loading()} fallback={
          <div class="bg-white shadow rounded-lg overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Day</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Progress</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                {expenses().map((expense) => (
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {expense.name}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {expense.amount ? `$${expense.amount.toFixed(2)}` : 'N/A'}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {getCategoryName(expense.category_id)}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span class={`px-2 py-1 text-xs rounded-full ${
                        expense.expense_type === 'ongoing' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'
                      }`}>
                        {expense.expense_type}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {expense.day_of_month}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {expense.expense_type === 'installment' && expense.total_payments
                        ? `${expense.payments_completed} / ${expense.total_payments}`
                        : '-'}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class={`px-2 py-1 text-xs rounded-full ${
                        expense.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {expense.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleToggleActive(expense)}
                        class="text-yellow-600 hover:text-yellow-900 mr-2"
                      >
                        {expense.is_active ? 'Deactivate' : 'Activate'}
                      </button>
                      <button
                        onClick={() => handleEdit(expense)}
                        class="text-indigo-600 hover:text-indigo-900 mr-2"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(expense.id)}
                        class="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {expenses().length === 0 && (
              <div class="text-center py-12 text-gray-500">No expenses found</div>
            )}
          </div>
        }>
          <div class="text-center py-12">Loading...</div>
        </Show>
      </div>
    </Layout>
  );
};

export default Expenses;

