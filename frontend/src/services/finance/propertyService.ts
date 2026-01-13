import api from '../../shared/services/api';

export interface Property {
  id: string;
  name: string;
  is_active: boolean;
  is_default: boolean;
  deleted_at?: string;
  created_at: string;
  updated_at: string;
}

export interface PropertyCreate {
  name: string;
  is_active?: boolean;
  is_default?: boolean;
}

export interface PropertyUpdate {
  name?: string;
  is_active?: boolean;
  is_default?: boolean;
}

export const propertyService = {
  async getAll(): Promise<Property[]> {
    const response = await api.get<Property[]>('/properties');
    return response.data;
  },

  async getById(id: string): Promise<Property> {
    const response = await api.get<Property>(`/properties/${id}`);
    return response.data;
  },

  async create(data: PropertyCreate): Promise<Property> {
    const response = await api.post<Property>('/properties', data);
    return response.data;
  },

  async update(id: string, data: PropertyUpdate): Promise<Property> {
    const response = await api.put<Property>(`/properties/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/properties/${id}`);
  },

  async getDefault(): Promise<Property | null> {
    const properties = await this.getAll();
    const defaultProperty = properties.find(p => p.is_default);
    return defaultProperty || (properties.length > 0 ? properties[0] : null);
  },
};

