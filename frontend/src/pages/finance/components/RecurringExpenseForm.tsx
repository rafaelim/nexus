import { createSignal, Show } from 'solid-js';
import { recurringExpenseService } from '../../../services/finance/recurringExpenseService';
import type { RecurringExpense, RecurringExpenseCreate, RecurringExpenseUpdate } from '../../../services/finance/recurringExpenseService';
import type { Category } from '../../../services/finance/categoryService';
import { format } from 'date-fns';

interface RecurringExpenseFormProps {
  expense?: RecurringExpense | null;
  categories: Category[];
  onClose: () => void;
  onSubmit: () => void;
  defaultExpenseType?: 'ongoing' | 'installment';
}

const RecurringExpenseForm = (props: RecurringExpenseFormProps) => {
  const [name, setName] = createSignal(props.expense?.name || '');
  const [amount, setAmount] = createSignal(props.expense?.amount?.toString() || '');
  const [categoryId, setCategoryId] = createSignal(props.expense?.category_id || '');
  const [dayOfMonth, setDayOfMonth] = createSignal(props.expense?.day_of_month.toString() || '1');
  const [expenseType, setExpenseType] = createSignal<'ongoing' | 'installment'>(
    props.expense?.expense_type || props.defaultExpenseType || 'ongoing'
  );
  const [startDate, setStartDate] = createSignal(
    props.expense?.start_date ? format(new Date(props.expense.start_date), 'yyyy-MM-dd') : format(new Date(), 'yyyy-MM-dd')
  );
  const [totalPayments, setTotalPayments] = createSignal(
    props.expense?.total_payments?.toString() || ''
  );
  const [notes, setNotes] = createSignal(props.expense?.notes || '');
  const [loading, setLoading] = createSignal(false);
  const [error, setError] = createSignal('');

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (props.expense) {
        const updateData: RecurringExpenseUpdate = {
          name: name(),
          amount: amount() ? parseFloat(amount()) : undefined,
          category_id: categoryId(),
          day_of_month: parseInt(dayOfMonth()),
          expense_type: expenseType(),
          start_date: startDate(),
          total_payments: expenseType() === 'installment' && totalPayments() ? parseInt(totalPayments()) : undefined,
          notes: notes() || undefined,
        };
        await recurringExpenseService.update(props.expense.id, updateData);
      } else {
        const createData: RecurringExpenseCreate = {
          name: name(),
          amount: amount() ? parseFloat(amount()) : undefined,
          category_id: categoryId(),
          day_of_month: parseInt(dayOfMonth()),
          expense_type: expenseType(),
          start_date: startDate(),
          total_payments: expenseType() === 'installment' && totalPayments() ? parseInt(totalPayments()) : undefined,
          notes: notes() || undefined,
        };
        await recurringExpenseService.create(createData);
      }
      props.onSubmit();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save recurring expense');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white m-4">
        <h3 class="text-lg font-bold mb-4">
          {props.expense ? 'Edit Recurring Expense' : 'Create Recurring Expense'}
        </h3>
        <form onSubmit={handleSubmit}>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <input
              type="text"
              required
              value={name()}
              onInput={(e) => setName(e.currentTarget.value)}
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Amount (optional)</label>
              <input
                type="number"
                step="0.01"
                value={amount()}
                onInput={(e) => setAmount(e.currentTarget.value)}
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="Leave empty if variable"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Day of Month</label>
              <input
                type="number"
                min="1"
                max="31"
                required
                value={dayOfMonth()}
                onInput={(e) => setDayOfMonth(e.currentTarget.value)}
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select
              required
              value={categoryId()}
              onChange={(e) => setCategoryId(e.currentTarget.value)}
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="">Select a category</option>
              {props.categories.map((cat) => (
                <option value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Expense Type</label>
            <select
              required
              value={expenseType()}
              onChange={(e) => setExpenseType(e.currentTarget.value as 'ongoing' | 'installment')}
              disabled={!!props.defaultExpenseType}
              class="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-100 disabled:cursor-not-allowed"
            >
              <option value="ongoing">Ongoing</option>
              <option value="installment">Installment</option>
            </select>
            {props.defaultExpenseType && (
              <p class="mt-1 text-xs text-gray-500">
                Expense type is set based on the current page
              </p>
            )}
          </div>
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input
                type="date"
                required
                value={startDate()}
                onInput={(e) => setStartDate(e.currentTarget.value)}
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <Show when={expenseType() === 'installment'}>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Total Payments</label>
                <input
                  type="number"
                  min="1"
                  required={expenseType() === 'installment'}
                  value={totalPayments()}
                  onInput={(e) => setTotalPayments(e.currentTarget.value)}
                  class="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
            </Show>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
            <textarea
              value={notes()}
              onInput={(e) => setNotes(e.currentTarget.value)}
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
              rows="3"
            />
          </div>
          {error() && <div class="text-red-600 text-sm mb-4">{error()}</div>}
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              onClick={props.onClose}
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading()}
              class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {loading() ? 'Saving...' : 'Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RecurringExpenseForm;

