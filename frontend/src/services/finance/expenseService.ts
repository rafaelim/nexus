import api from '../../shared/services/api';

export interface Expense {
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

export interface ExpenseCreate {
  name: string;
  amount?: number;
  category_id: string;
  day_of_month: number;
  expense_type: 'ongoing' | 'installment';
  start_date: string;
  total_payments?: number;
  notes?: string;
}

export interface ExpenseUpdate {
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

export const expenseService = {
  async getAll(is_active?: boolean): Promise<Expense[]> {
    const response = await api.get<Expense[]>('/expenses', {
      params: is_active !== undefined ? { is_active } : {},
    });
    return response.data;
  },

  async getById(id: string): Promise<Expense> {
    const response = await api.get<Expense>(`/expenses/${id}`);
    return response.data;
  },

  async create(data: ExpenseCreate): Promise<Expense> {
    const response = await api.post<Expense>('/expenses', data);
    return response.data;
  },

  async update(id: string, data: ExpenseUpdate): Promise<Expense> {
    const response = await api.put<Expense>(`/expenses/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/expenses/${id}`);
  },

  async getByType(type: 'ongoing' | 'installment', is_active?: boolean): Promise<Expense[]> {
    const all = await this.getAll(is_active);
    return all.filter(exp => exp.expense_type === type);
  },
};

