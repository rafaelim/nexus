import { createSignal, onMount, Show } from 'solid-js';
import Layout from '../../../components/Layout';
import { categoryService } from '../../../services/finance/categoryService';
import type { Category } from '../../../services/finance/categoryService';
import CategoryForm from '../../../pages/finance/components/CategoryForm';
import { toastStore } from '../../../shared/stores/toastStore';

const Categories = () => {
  const [categories, setCategories] = createSignal<Category[]>([]);
  const [loading, setLoading] = createSignal(true);
  const [showForm, setShowForm] = createSignal(false);
  const [editingCategory, setEditingCategory] = createSignal<Category | null>(null);

  onMount(async () => {
    await loadCategories();
  });

  const loadCategories = async () => {
    try {
      setLoading(true);
      const data = await categoryService.getAll();
      setCategories(data);
    } catch (error) {
      console.error('Failed to load categories:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setEditingCategory(null);
    setShowForm(true);
  };

  const handleEdit = (category: Category) => {
    setEditingCategory(category);
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this category?')) return;
    try {
      await categoryService.delete(id);
      await loadCategories();
    } catch (error) {
      console.error('Failed to delete category:', error);
      toastStore.error('Failed to delete category');
    }
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingCategory(null);
  };

  const handleFormSubmit = async () => {
    await loadCategories();
    handleFormClose();
  };

  return (
    <Layout>
      <div class="max-w-7xl mx-auto">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-3xl font-bold text-gray-900">Categories</h1>
          <button
            onClick={handleCreate}
            class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
          >
            Add Category
          </button>
        </div>

        <Show when={showForm()}>
          <CategoryForm
            category={editingCategory()}
            onClose={handleFormClose}
            onSubmit={handleFormSubmit}
          />
        </Show>

        <Show when={loading()} fallback={
          <div class="bg-white shadow rounded-lg overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Color</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                {categories().map((category) => (
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {category.name}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span class={`px-2 py-1 text-xs rounded-full ${
                        category.type === 'income' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {category.type}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      {category.color && (
                        <div
                          class="w-6 h-6 rounded-full border border-gray-300"
                          style={{ 'background-color': category.color }}
                        />
                      )}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleEdit(category)}
                        class="text-indigo-600 hover:text-indigo-900 mr-4"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(category.id)}
                        class="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        }>
          <div class="text-center py-12">Loading...</div>
        </Show>
      </div>
    </Layout>
  );
};

export default Categories;

