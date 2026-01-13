import { createSignal, onMount, Show, createEffect } from 'solid-js';
import { transactionService } from '../../../services/finance/transactionService';
import type { Transaction, TransactionCreate } from '../../../services/finance/transactionService';
import type { Category } from '../../../services/finance/categoryService';
import type { Expense } from '../../../services/finance/expenseService';
import { expenseService } from '../../../services/finance/expenseService';
import { propertyService } from '../../../services/finance/propertyService';
import type { Property } from '../../../services/finance/propertyService';
import { format } from 'date-fns';

interface TransactionFormProps {
  transaction?: Transaction | null;
  categories: Category[];
  expenses?: Expense[];
  onClose: () => void;
  onSubmit: () => void;
}

const TransactionForm = (props: TransactionFormProps) => {
  const [date, setDate] = createSignal(
    props.transaction?.date ? format(new Date(props.transaction.date), 'yyyy-MM-dd') : format(new Date(), 'yyyy-MM-dd')
  );
  const [amount, setAmount] = createSignal(props.transaction?.amount.toString() || '');
  const [description, setDescription] = createSignal(props.transaction?.description || '');
  const [categoryId, setCategoryId] = createSignal(props.transaction?.category_id || '');
  const [propertyId, setPropertyId] = createSignal(props.transaction?.property_id || '');
  const [properties, setProperties] = createSignal<Property[]>([]);
  const [expenseId, setExpenseId] = createSignal(props.transaction?.expense_id || '');
  const [paymentMethod, setPaymentMethod] = createSignal(props.transaction?.payment_method || '');
  const [notes, setNotes] = createSignal(props.transaction?.notes || '');
  const [tags, setTags] = createSignal(props.transaction?.tags?.join(', ') || '');
  const [loading, setLoading] = createSignal(false);
  const [error, setError] = createSignal('');
  const [expenses, setExpenses] = createSignal<Expense[]>(props.expenses || []);

  // Load expenses and houses if not provided
  onMount(async () => {
    if (!props.expenses || props.expenses.length === 0) {
      try {
        const data = await expenseService.getAll(true); // Only active expenses
        setExpenses(data);
      } catch (error) {
        console.error('Failed to load expenses:', error);
      }
    }
    
    // Load properties and auto-select default
    try {
      const propertiesData = await propertyService.getAll();
      setProperties(propertiesData);
      
      // Auto-select default property if creating new transaction
      if (!props.transaction && !propertyId()) {
        const defaultProperty = await propertyService.getDefault();
        if (defaultProperty) {
          setPropertyId(defaultProperty.id);
        }
      }
    } catch (error) {
      console.error('Failed to load properties:', error);
    }
  });

  // Pre-fill form when expense is selected
  createEffect(() => {
    if (expenseId() && !props.transaction) {
      const selectedExpense = expenses().find(exp => exp.id === expenseId());
      if (selectedExpense) {
        if (!amount() && selectedExpense.amount) {
          setAmount(selectedExpense.amount.toString());
        }
        if (!description()) {
          setDescription(selectedExpense.name);
        }
        if (!categoryId()) {
          setCategoryId(selectedExpense.category_id);
        }
        if (!notes() && selectedExpense.notes) {
          setNotes(selectedExpense.notes);
        }
      }
    }
  });

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const tagsArray = tags().split(',').map(t => t.trim()).filter(t => t);
      
      // Transactions cannot be updated, only created
      const createData: TransactionCreate = {
        date: date(),
        amount: parseFloat(amount()),
        description: description() || undefined,
        category_id: categoryId(),
        property_id: propertyId(),
        expense_id: expenseId() || undefined,
        payment_method: paymentMethod() || undefined,
        notes: notes() || undefined,
        tags: tagsArray.length > 0 ? tagsArray : undefined,
      };
      await transactionService.create(createData);
      props.onSubmit();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save transaction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white m-4">
        <h3 class="text-lg font-bold mb-4">
          Create Transaction
        </h3>
        <form onSubmit={handleSubmit}>
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
              <input
                type="date"
                required
                value={date()}
                onInput={(e) => setDate(e.currentTarget.value)}
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Amount</label>
              <input
                type="number"
                step="0.01"
                required
                value={amount()}
                onInput={(e) => setAmount(e.currentTarget.value)}
                class="w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Property *</label>
            <select
              required
              value={propertyId()}
              onChange={(e) => setPropertyId(e.currentTarget.value)}
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="">Select a property</option>
              {properties().map((property) => (
                <option value={property.id}>
                  {property.name} {property.is_default ? '(Default)' : ''}
                </option>
              ))}
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Expense (optional)</label>
            <select
              value={expenseId()}
              onChange={(e) => setExpenseId(e.currentTarget.value)}
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="">None - Manual Transaction</option>
              {expenses().map((exp) => (
                <option value={exp.id}>
                  {exp.name} ({exp.expense_type === 'ongoing' ? 'Ongoing' : `Installment ${exp.payments_completed}/${exp.total_payments || 0}`})
                </option>
              ))}
            </select>
            <p class="mt-1 text-xs text-gray-500">
              Selecting an expense will pre-fill the form. You can still edit all fields.
            </p>
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
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <input
              type="text"
              value={description()}
              onInput={(e) => setDescription(e.currentTarget.value)}
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Payment Method</label>
            <input
              type="text"
              value={paymentMethod()}
              onInput={(e) => setPaymentMethod(e.currentTarget.value)}
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Tags (comma-separated)</label>
            <input
              type="text"
              value={tags()}
              onInput={(e) => setTags(e.currentTarget.value)}
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="tag1, tag2, tag3"
            />
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

export default TransactionForm;

