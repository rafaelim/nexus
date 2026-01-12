import api from '../../shared/services/api';

export interface RecurringExpense {
  id: string;
  user_id: string;
  name: string;
  amount?: number;
  category_id: string;
  day_of_month: number;
  expense_type: 'ongoing' | 'installment';
  start_date: string;
  total_payments?: number;
  payments_completed: number;
  is_active: boolean;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface RecurringExpenseCreate {
  name: string;
  amount?: number;
  category_id: string;
  day_of_month: number;
  expense_type: 'ongoing' | 'installment';
  start_date: string;
  total_payments?: number;
  notes?: string;
}

export interface RecurringExpenseUpdate {
  name?: string;
  amount?: number;
  category_id?: string;
  day_of_month?: number;
  expense_type?: 'ongoing' | 'installment';
  start_date?: string;
  total_payments?: number;
  is_active?: boolean;
  notes?: string;
}

export interface GenerateTransactionRequest {
  date: string;
  notes?: string;
}

export const recurringExpenseService = {
  async getAll(is_active?: boolean): Promise<RecurringExpense[]> {
    const response = await api.get<RecurringExpense[]>('/recurring-expenses', {
      params: is_active !== undefined ? { is_active } : {},
    });
    return response.data;
  },

  async getById(id: string): Promise<RecurringExpense> {
    const response = await api.get<RecurringExpense>(`/recurring-expenses/${id}`);
    return response.data;
  },

  async create(data: RecurringExpenseCreate): Promise<RecurringExpense> {
    const response = await api.post<RecurringExpense>('/recurring-expenses', data);
    return response.data;
  },

  async update(id: string, data: RecurringExpenseUpdate): Promise<RecurringExpense> {
    const response = await api.put<RecurringExpense>(`/recurring-expenses/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/recurring-expenses/${id}`);
  },

  async generateTransaction(id: string, data: GenerateTransactionRequest) {
    const response = await api.post(`/recurring-expenses/${id}/generate-transaction`, data);
    return response.data;
  },

  async getByType(type: 'ongoing' | 'installment', is_active?: boolean): Promise<RecurringExpense[]> {
    const all = await this.getAll(is_active);
    return all.filter(exp => exp.expense_type === type);
  },
};

