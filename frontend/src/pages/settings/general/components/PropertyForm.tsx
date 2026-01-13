import { createSignal, onMount, Show } from 'solid-js';
import type { Property, PropertyCreate, PropertyUpdate } from '../../../../services/finance/propertyService';
import { propertyService } from '../../../../services/finance/propertyService';
import { toastStore } from '../../../../shared/stores/toastStore';

interface PropertyFormProps {
  property: Property | null;
  onClose: () => void;
  onSubmit: () => void;
}

const PropertyForm = (props: PropertyFormProps) => {
  const [name, setName] = createSignal(props.property?.name || '');
  const [isActive, setIsActive] = createSignal(props.property?.is_active ?? true);
  const [isDefault, setIsDefault] = createSignal(props.property?.is_default ?? false);
  const [loading, setLoading] = createSignal(false);
  const [allProperties, setAllProperties] = createSignal<Property[]>([]);

  onMount(async () => {
    // Load all properties to check if we can set default
    const properties = await propertyService.getAll();
    setAllProperties(properties);
    
    // If creating and no properties exist, auto-set as default
    if (!props.property && properties.length === 0) {
      setIsDefault(true);
    }
  });

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    
    if (!name().trim()) {
      toastStore.error('Property name is required');
      return;
    }

    setLoading(true);
    try {
      if (props.property) {
        const updateData: PropertyUpdate = {
          name: name(),
          is_active: isActive(),
          is_default: isDefault(),
        };
        await propertyService.update(props.property.id, updateData);
        toastStore.success('Property updated successfully');
      } else {
        const createData: PropertyCreate = {
          name: name(),
          is_active: isActive(),
          is_default: isDefault(),
        };
        await propertyService.create(createData);
        toastStore.success('Property created successfully');
      }
      props.onSubmit();
    } catch (error: any) {
      console.error('Failed to save property:', error);
      toastStore.error(error.response?.data?.detail || 'Failed to save property');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">
          {props.property ? 'Edit Property' : 'Create Property'}
        </h2>
        
        <form onSubmit={handleSubmit}>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Name *
            </label>
            <input
              type="text"
              value={name()}
              onInput={(e) => setName(e.currentTarget.value)}
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              required
            />
          </div>

          <div class="mb-4">
            <label class="flex items-center">
              <input
                type="checkbox"
                checked={isActive()}
                onChange={(e) => setIsActive(e.currentTarget.checked)}
                class="mr-2"
              />
              <span class="text-sm font-medium text-gray-700">Active</span>
            </label>
          </div>

          <div class="mb-4">
            <label class="flex items-center">
              <input
                type="checkbox"
                checked={isDefault()}
                onChange={(e) => setIsDefault(e.currentTarget.checked)}
                class="mr-2"
              />
              <span class="text-sm font-medium text-gray-700">Default</span>
            </label>
            <p class="text-xs text-gray-500 mt-1">
              Only one property can be default at a time
            </p>
          </div>

          <div class="flex justify-end space-x-3">
            <button
              type="button"
              onClick={props.onClose}
              class="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
              disabled={loading()}
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
              disabled={loading()}
            >
              {loading() ? 'Saving...' : props.property ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PropertyForm;

