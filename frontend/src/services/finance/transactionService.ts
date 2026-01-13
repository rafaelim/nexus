import api from '../../shared/services/api';

export interface Transaction {
  id: string;
  user_id: string;
  property_id: string;
  date: string;
  amount: number;
  description?: string;
  category_id: string;
  expense_id?: string;
  tags?: string[];
  payment_method?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface TransactionCreate {
  date: string;
  amount: number;
  description?: string;
  category_id: string;
  property_id: string;
  expense_id?: string;
  tags?: string[];
  payment_method?: string;
  notes?: string;
}

export interface TransactionUpdate {
  date?: string;
  amount?: number;
  description?: string;
  category_id?: string;
  tags?: string[];
  payment_method?: string;
  notes?: string;
}

export const transactionService = {
  async getAll(params?: {
    start_date?: string;
    end_date?: string;
    category_id?: string;
    limit?: number;
    offset?: number;
  }): Promise<Transaction[]> {
    const response = await api.get<Transaction[]>('/transactions', { params });
    return response.data;
  },

  async getById(id: string): Promise<Transaction> {
    const response = await api.get<Transaction>(`/transactions/${id}`);
    return response.data;
  },

  async create(data: TransactionCreate): Promise<Transaction> {
    const response = await api.post<Transaction>('/transactions', data);
    return response.data;
  },

  async update(id: string, data: TransactionUpdate): Promise<Transaction> {
    const response = await api.put<Transaction>(`/transactions/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/transactions/${id}`);
  },
};

