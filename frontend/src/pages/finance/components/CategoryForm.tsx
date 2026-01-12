import { createSignal, onMount, Show } from 'solid-js';
import { categoryService } from '../../../services/finance/categoryService';
import type { Category, CategoryCreate, CategoryUpdate } from '../../../services/finance/categoryService';

interface CategoryFormProps {
  category?: Category | null;
  onClose: () => void;
  onSubmit: () => void;
}

const generateRandomColor = (): string => {
  // Generate a random hex color
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};

const CategoryForm = (props: CategoryFormProps) => {
  const [name, setName] = createSignal(props.category?.name || '');
  const [type, setType] = createSignal<'income' | 'expense'>(props.category?.type || 'expense');
  // Initialize with random color for new categories, existing color for edits
  const [color, setColor] = createSignal(
    props.category?.color || generateRandomColor()
  );
  const [loading, setLoading] = createSignal(false);
  const [error, setError] = createSignal('');

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (props.category) {
        const updateData: CategoryUpdate = {
          name: name(),
          type: type(),
          color: color() || undefined,
        };
        await categoryService.update(props.category.id, updateData);
      } else {
        const createData: CategoryCreate = {
          name: name(),
          type: type(),
          color: color() || undefined,
        };
        await categoryService.create(createData);
      }
      props.onSubmit();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save category');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <h3 class="text-lg font-bold mb-4">
          {props.category ? 'Edit Category' : 'Create Category'}
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
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
            <select
              value={type()}
              onChange={(e) => setType(e.currentTarget.value as 'income' | 'expense')}
              class="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="expense">Expense</option>
              <option value="income">Income</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Color (hex)</label>
            <input
              type="color"
              value={color() || '#000000'}
              onInput={(e) => setColor(e.currentTarget.value)}
              class="w-full h-10 border border-gray-300 rounded-md"
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

export default CategoryForm;

