import { createSignal, onMount, Show } from 'solid-js';
import Layout from '../../components/Layout';
import { transactionService } from '../../services/finance/transactionService';
import type { Transaction, TransactionCreate } from '../../services/finance/transactionService';
import { categoryService } from '../../services/finance/categoryService';
import type { Category } from '../../services/finance/categoryService';
import TransactionForm from './components/TransactionForm';
import TransactionList from './components/TransactionList';
import { format } from 'date-fns';
import { toastStore } from '../../shared/stores/toastStore';

const Transactions = () => {
  const [transactions, setTransactions] = createSignal<Transaction[]>([]);
  const [categories, setCategories] = createSignal<Category[]>([]);
  const [loading, setLoading] = createSignal(true);
  const [showForm, setShowForm] = createSignal(false);
  const [editingTransaction, setEditingTransaction] = createSignal<Transaction | null>(null);
  const [startDate, setStartDate] = createSignal('');
  const [endDate, setEndDate] = createSignal('');
  const [selectedCategory, setSelectedCategory] = createSignal<string>('');

  onMount(async () => {
    await Promise.all([loadTransactions(), loadCategories()]);
  });

  const loadCategories = async () => {
    try {
      const data = await categoryService.getAll();
      setCategories(data);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (startDate()) params.start_date = startDate();
      if (endDate()) params.end_date = endDate();
      if (selectedCategory()) params.category_id = selectedCategory();
      
      const data = await transactionService.getAll(params);
      setTransactions(data);
    } catch (error) {
      console.error('Failed to load transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setEditingTransaction(null);
    setShowForm(true);
  };

  const handleEdit = (transaction: Transaction) => {
    setEditingTransaction(transaction);
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this transaction?')) return;
    try {
      await transactionService.delete(id);
      await loadTransactions();
    } catch (error) {
      console.error('Failed to delete transaction:', error);
      toastStore.error('Failed to delete transaction');
    }
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingTransaction(null);
  };

  const handleFormSubmit = async () => {
    await loadTransactions();
    handleFormClose();
  };

  const handleFilter = () => {
    loadTransactions();
  };

  return (
    <Layout>
      <div class="max-w-7xl mx-auto">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-3xl font-bold text-gray-900">Transactions</h1>
          <button
            onClick={handleCreate}
            class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
          >
            Add Transaction
          </button>
        </div>

        <div class="bg-white p-4 rounded-lg shadow mb-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input
                type="date"
                value={startDate()}
                onInput={(e) => setStartDate(e.currentTarget.value)}
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
              <input
                type="date"
                value={endDate()}
                onInput={(e) => setEndDate(e.currentTarget.value)}
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select
                value={selectedCategory()}
                onChange={(e) => setSelectedCategory(e.currentTarget.value)}
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="">All Categories</option>
                {categories().map((cat) => (
                  <option value={cat.id}>{cat.name}</option>
                ))}
              </select>
            </div>
            <div class="flex items-end">
              <button
                onClick={handleFilter}
                class="w-full bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md"
              >
                Filter
              </button>
            </div>
          </div>
        </div>

        <Show when={showForm()}>
          <TransactionForm
            transaction={editingTransaction()}
            categories={categories()}
            onClose={handleFormClose}
            onSubmit={handleFormSubmit}
          />
        </Show>

        <Show when={loading()} fallback={
          <TransactionList
            transactions={transactions()}
            categories={categories()}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        }>
          <div class="text-center py-12">Loading...</div>
        </Show>
      </div>
    </Layout>
  );
};

export default Transactions;

