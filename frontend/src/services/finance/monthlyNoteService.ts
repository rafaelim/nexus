import api from '../../shared/services/api';

export interface MonthlyNote {
  id: string;
  user_id: string;
  domain: string;
  year: number;
  month: number;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface MonthlyNoteCreate {
  domain?: string;
  year: number;
  month: number;
  notes: string;
}

export interface MonthlyNoteUpdate {
  notes?: string;
}

export const monthlyNoteService = {
  async getAll(domain: string = 'finance'): Promise<MonthlyNote[]> {
    const response = await api.get<MonthlyNote[]>('/monthly-notes', {
      params: { domain },
    });
    return response.data;
  },

  async getByPeriod(year: number, month: number, domain: string = 'finance'): Promise<MonthlyNote | null> {
    try {
      const response = await api.get<MonthlyNote>(`/monthly-notes/${year}/${month}`, {
        params: { domain },
      });
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null;
      }
      throw error;
    }
  },

  async createOrUpdate(data: MonthlyNoteCreate): Promise<MonthlyNote> {
    const response = await api.post<MonthlyNote>('/monthly-notes', data);
    return response.data;
  },

  async update(id: string, data: MonthlyNoteUpdate): Promise<MonthlyNote> {
    const response = await api.put<MonthlyNote>(`/monthly-notes/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/monthly-notes/${id}`);
  },
};

