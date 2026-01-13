import { Router, Route } from '@solidjs/router';
import './index.css';
import Home from './pages/Home';
import Dashboard from './pages/finance/Dashboard';
import Transactions from './pages/finance/Transactions';
import Expenses from './pages/finance/Expenses';
import MonthlyNotes from './pages/finance/MonthlyNotes';
import Settings from './pages/settings/Settings';
import FinanceSettings from './pages/settings/finance/FinanceSettings';
import Categories from './pages/settings/finance/Categories';
import Toast from './components/Toast';

function App() {
  return (
    <>
      <Router>
        <Route path="/" component={Home} />
        <Route path="/expenses" component={Dashboard} />
        <Route path="/expenses/transactions" component={Transactions} />
        <Route path="/expenses/expenses" component={Expenses} />
        <Route path="/expenses/monthly-notes" component={MonthlyNotes} />
        <Route path="/settings" component={Settings} />
        <Route path="/settings/finance" component={FinanceSettings} />
        <Route path="/settings/finance/categories" component={Categories} />
      </Router>
      <Toast />
    </>
  );
}

export default App;
