import { createSignal, onMount, Show } from 'solid-js';
import Layout from '../../components/Layout';
import { transactionService } from '../../services/finance/transactionService';
import type { Transaction } from '../../services/finance/transactionService';
import { categoryService } from '../../services/finance/categoryService';
import type { Category } from '../../services/finance/categoryService';
import { recurringExpenseService } from '../../services/finance/recurringExpenseService';
import type { RecurringExpense } from '../../services/finance/recurringExpenseService';
import { monthlyNoteService } from '../../services/finance/monthlyNoteService';
import type { MonthlyNote } from '../../services/finance/monthlyNoteService';
import ExpenseByCategoryChart from './components/charts/ExpenseByCategoryChart';
import MonthlyTrendChart from './components/charts/MonthlyTrendChart';
import { format, startOfMonth, endOfMonth, subMonths } from 'date-fns';

const Dashboard = () => {
  const [transactions, setTransactions] = createSignal<Transaction[]>([]);
  const [categories, setCategories] = createSignal<Category[]>([]);
  const [recurringExpenses, setRecurringExpenses] = createSignal<RecurringExpense[]>([]);
  const [monthlyNote, setMonthlyNote] = createSignal<MonthlyNote | null>(null);
  const [loading, setLoading] = createSignal(true);
  const [monthFilter, setMonthFilter] = createSignal(format(new Date(), 'yyyy-MM'));

  onMount(async () => {
    try {
      await Promise.all([loadTransactions(), loadCategories(), loadRecurringExpenses(), loadMonthlyNote()]);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      setLoading(false); // Ensure loading is set to false even on error
    }
  });

  const loadCategories = async () => {
    try {
      const data = await categoryService.getAll();
      setCategories(data);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const loadRecurringExpenses = async () => {
    try {
      const data = await recurringExpenseService.getAll(true);
      setRecurringExpenses(data);
    } catch (error) {
      console.error('Failed to load recurring expenses:', error);
    }
  };

  const loadMonthlyNote = async () => {
    try {
      const [year, month] = monthFilter().split('-');
      const note = await monthlyNoteService.getByPeriod(parseInt(year), parseInt(month), 'finance');
      setMonthlyNote(note);
    } catch (error) {
      console.error('Failed to load monthly note:', error);
    }
  };

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const [year, month] = monthFilter().split('-');
      const start = startOfMonth(new Date(parseInt(year), parseInt(month) - 1));
      const end = endOfMonth(new Date(parseInt(year), parseInt(month) - 1));
      
      const data = await transactionService.getAll({
        start_date: format(start, 'yyyy-MM-dd'),
        end_date: format(end, 'yyyy-MM-dd'),
      });
      setTransactions(data);
    } catch (error) {
      console.error('Failed to load transactions:', error);
      setTransactions([]); // Set empty array on error
    } finally {
      setLoading(false);
    }
  };

  const getCategoryName = (categoryId: string) => {
    const category = categories().find(c => c.id === categoryId);
    return category?.name || 'Unknown';
  };

  const getCategoryType = (categoryId: string) => {
    const category = categories().find(c => c.id === categoryId);
    return category?.type || 'expense';
  };

  const calculateSummary = () => {
    const monthTransactions = transactions();
    let income = 0;
    let expense = 0;

    monthTransactions.forEach(tx => {
      const type = getCategoryType(tx.category_id);
      if (type === 'income') {
        income += tx.amount;
      } else {
        expense += tx.amount;
      }
    });

    return { income, expense, net: income - expense };
  };

  const getExpenseByCategory = () => {
    const expenseCategories = new Map<string, number>();
    transactions().forEach(tx => {
      const type = getCategoryType(tx.category_id);
      if (type === 'expense') {
        const categoryName = getCategoryName(tx.category_id);
        expenseCategories.set(categoryName, (expenseCategories.get(categoryName) || 0) + tx.amount);
      }
    });
    return Array.from(expenseCategories.entries()).map(([category, amount]) => ({
      category,
      amount,
    }));
  };

  const getMonthlyTrend = () => {
    const months = [];
    for (let i = 5; i >= 0; i--) {
      const month = subMonths(new Date(), i);
      months.push(format(month, 'MMM yyyy'));
    }
    
    // This is a simplified version - in production, you'd fetch data for each month
    return months.map(month => ({
      month,
      income: Math.random() * 5000,
      expense: Math.random() * 4000,
    }));
  };

  const summary = () => calculateSummary();
  const expenseByCategory = () => getExpenseByCategory();
  const monthlyTrend = () => getMonthlyTrend();
  const recentTransactions = () => transactions().slice(0, 5);
  const upcomingExpenses = () => {
    const today = new Date();
    const dayOfMonth = today.getDate();
    return recurringExpenses()
      .filter(exp => exp.is_active && exp.day_of_month >= dayOfMonth)
      .sort((a, b) => a.day_of_month - b.day_of_month)
      .slice(0, 5);
  };

  return (
    <Layout>
      <div class="max-w-7xl mx-auto">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
          <div>
            <input
              type="month"
              value={monthFilter()}
              onInput={(e) => {
                setMonthFilter(e.currentTarget.value);
                loadTransactions();
                loadMonthlyNote();
              }}
              class="px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
        </div>

        <Show when={!loading()}>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div class="bg-white p-6 rounded-lg shadow">
              <h3 class="text-sm font-medium text-gray-500 mb-2">Total Income</h3>
              <p class="text-3xl font-bold text-green-600">${summary().income.toFixed(2)}</p>
            </div>
            <div class="bg-white p-6 rounded-lg shadow">
              <h3 class="text-sm font-medium text-gray-500 mb-2">Total Expenses</h3>
              <p class="text-3xl font-bold text-red-600">${summary().expense.toFixed(2)}</p>
            </div>
            <div class="bg-white p-6 rounded-lg shadow">
              <h3 class="text-sm font-medium text-gray-500 mb-2">Net</h3>
              <p class={`text-3xl font-bold ${summary().net >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                ${summary().net.toFixed(2)}
              </p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div class="bg-white p-6 rounded-lg shadow">
              <ExpenseByCategoryChart data={expenseByCategory()} type="bar" />
            </div>
            <div class="bg-white p-6 rounded-lg shadow">
              <MonthlyTrendChart data={monthlyTrend()} />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div class="bg-white p-6 rounded-lg shadow">
              <h3 class="text-lg font-semibold mb-4">Recent Transactions</h3>
              <div class="space-y-2">
                {recentTransactions().map((tx) => {
                  const isIncome = getCategoryType(tx.category_id) === 'income';
                  return (
                    <div class="flex justify-between items-center py-2 border-b">
                      <div class="flex-1">
                        <p class="text-sm font-medium">{tx.description || 'No description'}</p>
                        <p class="text-xs text-gray-500">{getCategoryName(tx.category_id)}</p>
                        {tx.notes && (
                          <p class="text-xs text-gray-400 mt-1 italic">{tx.notes}</p>
                        )}
                      </div>
                      <p class={`text-sm font-medium ${isIncome ? 'text-green-600' : 'text-red-600'}`}>
                        {isIncome ? '+' : '-'}${Math.abs(tx.amount).toFixed(2)}
                      </p>
                    </div>
                  );
                })}
                {recentTransactions().length === 0 && (
                  <p class="text-sm text-gray-500">No transactions</p>
                )}
              </div>
            </div>

            <div class="bg-white p-6 rounded-lg shadow">
              <h3 class="text-lg font-semibold mb-4">Upcoming Recurring Expenses</h3>
              <div class="space-y-2">
                {upcomingExpenses().map((exp) => (
                  <div class="flex justify-between items-center py-2 border-b">
                    <div class="flex-1">
                      <p class="text-sm font-medium">{exp.name}</p>
                      <p class="text-xs text-gray-500">Day {exp.day_of_month}</p>
                      {exp.notes && (
                        <p class="text-xs text-gray-400 mt-1 italic">{exp.notes}</p>
                      )}
                    </div>
                    <p class="text-sm font-medium text-gray-900">
                      {exp.amount ? `$${exp.amount.toFixed(2)}` : 'N/A'}
                    </p>
                  </div>
                ))}
                {upcomingExpenses().length === 0 && (
                  <p class="text-sm text-gray-500">No upcoming expenses</p>
                )}
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-lg shadow">
            <h3 class="text-lg font-semibold mb-4">Monthly Notes</h3>
            <Show when={monthlyNote()} fallback={
              <p class="text-sm text-gray-500">No notes for this month</p>
            }>
              <div class="prose max-w-none">
                <p class="text-sm text-gray-700 whitespace-pre-wrap">{monthlyNote()?.notes}</p>
              </div>
            </Show>
          </div>
        </Show>

        <Show when={loading()}>
          <div class="text-center py-12">Loading...</div>
        </Show>
      </div>
    </Layout>
  );
};

export default Dashboard;

