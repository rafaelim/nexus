import type { Transaction } from '../../../services/finance/transactionService';
import type { Category } from '../../../services/finance/categoryService';
import { format } from 'date-fns';

interface TransactionListProps {
  transactions: Transaction[];
  categories: Category[];
  onEdit: (transaction: Transaction) => void;
  onDelete: (id: string) => void;
}

const TransactionList = (props: TransactionListProps) => {
  const getCategoryName = (categoryId: string) => {
    const category = props.categories.find(c => c.id === categoryId);
    return category?.name || 'Unknown';
  };

  const getCategoryType = (categoryId: string) => {
    const category = props.categories.find(c => c.id === categoryId);
    return category?.type || 'expense';
  };

  return (
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Amount</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          {props.transactions.map((transaction) => {
            const isIncome = getCategoryType(transaction.category_id) === 'income';
            return (
              <tr>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {format(new Date(transaction.date), 'MMM dd, yyyy')}
                </td>
                <td class="px-6 py-4 text-sm text-gray-900">
                  {transaction.description || '-'}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {getCategoryName(transaction.category_id)}
                </td>
                <td class={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${
                  isIncome ? 'text-green-600' : 'text-red-600'
                }`}>
                  {isIncome ? '+' : '-'}${Math.abs(transaction.amount).toFixed(2)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    onClick={() => props.onEdit(transaction)}
                    class="text-indigo-600 hover:text-indigo-900 mr-4"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => props.onDelete(transaction.id)}
                    class="text-red-600 hover:text-red-900"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      {props.transactions.length === 0 && (
        <div class="text-center py-12 text-gray-500">No transactions found</div>
      )}
    </div>
  );
};

export default TransactionList;

