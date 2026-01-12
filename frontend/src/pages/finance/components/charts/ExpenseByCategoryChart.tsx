import { onMount, createSignal } from 'solid-js';
import {
  Chart,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Pie } from 'solid-chartjs';

Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

interface ExpenseByCategoryChartProps {
  data: { category: string; amount: number }[];
  type?: 'bar' | 'pie';
}

const ExpenseByCategoryChart = (props: ExpenseByCategoryChartProps) => {
  const chartData = () => ({
    labels: props.data.map(d => d.category),
    datasets: [
      {
        label: 'Amount',
        data: props.data.map(d => d.amount),
        backgroundColor: [
          'rgba(239, 68, 68, 0.8)',
          'rgba(249, 115, 22, 0.8)',
          'rgba(234, 179, 8, 0.8)',
          'rgba(34, 197, 94, 0.8)',
          'rgba(59, 130, 246, 0.8)',
          'rgba(147, 51, 234, 0.8)',
          'rgba(236, 72, 153, 0.8)',
        ],
      },
    ],
  });

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Expenses by Category',
      },
    },
  };

  return (
    <div class="h-64">
      {props.type === 'pie' ? (
        <Pie data={chartData()} options={chartOptions} />
      ) : (
        <Bar data={chartData()} options={chartOptions} />
      )}
    </div>
  );
};

export default ExpenseByCategoryChart;

