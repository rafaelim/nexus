import { createSignal, onMount, Show } from 'solid-js';
import Layout from '../../../components/Layout';
import { propertyService } from '../../../services/finance/propertyService';
import type { Property } from '../../../services/finance/propertyService';
import PropertyForm from './components/PropertyForm';
import { toastStore } from '../../../shared/stores/toastStore';

const Properties = () => {
  const [properties, setProperties] = createSignal<Property[]>([]);
  const [loading, setLoading] = createSignal(true);
  const [showForm, setShowForm] = createSignal(false);
  const [editingProperty, setEditingProperty] = createSignal<Property | null>(null);

  onMount(async () => {
    await loadProperties();
  });

  const loadProperties = async () => {
    try {
      setLoading(true);
      const data = await propertyService.getAll();
      setProperties(data);
    } catch (error) {
      console.error('Failed to load properties:', error);
      toastStore.error('Failed to load properties');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setEditingProperty(null);
    setShowForm(true);
  };

  const handleEdit = (property: Property) => {
    setEditingProperty(property);
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this property?')) return;
    try {
      await propertyService.delete(id);
      await loadProperties();
      toastStore.success('Property deleted successfully');
    } catch (error) {
      console.error('Failed to delete property:', error);
      toastStore.error('Failed to delete property');
    }
  };

  const handleSetDefault = async (id: string) => {
    try {
      await propertyService.update(id, { is_default: true });
      await loadProperties();
      toastStore.success('Default property updated');
    } catch (error) {
      console.error('Failed to set default property:', error);
      toastStore.error('Failed to set default property');
    }
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingProperty(null);
  };

  const handleFormSubmit = async () => {
    await loadProperties();
    handleFormClose();
  };

  return (
    <Layout>
      <div class="max-w-7xl mx-auto">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-3xl font-bold text-gray-900">Properties</h1>
          <button
            onClick={handleCreate}
            class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
          >
            Add Property
          </button>
        </div>

        <Show when={showForm()}>
          <PropertyForm
            property={editingProperty()}
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
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Active</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Default</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                {properties().map((property) => (
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {property.name}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span class={`px-2 py-1 text-xs rounded-full ${
                        property.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {property.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {property.is_default && (
                        <span class="px-2 py-1 text-xs rounded-full bg-indigo-100 text-indigo-800">
                          Default
                        </span>
                      )}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <Show when={!property.is_default}>
                        <button
                          onClick={() => handleSetDefault(property.id)}
                          class="text-indigo-600 hover:text-indigo-900 mr-4"
                        >
                          Set Default
                        </button>
                      </Show>
                      <button
                        onClick={() => handleEdit(property)}
                        class="text-indigo-600 hover:text-indigo-900 mr-4"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(property.id)}
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

export default Properties;

