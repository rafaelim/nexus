import { Router, Route } from '@solidjs/router';
import './index.css';
import Home from './pages/Home';
import Dashboard from './pages/finance/Dashboard';
import Transactions from './pages/finance/Transactions';
import Categories from './pages/finance/Categories';
import OngoingExpenses from './pages/finance/OngoingExpenses';
import InstallmentExpenses from './pages/finance/InstallmentExpenses';
import MonthlyNotes from './pages/finance/MonthlyNotes';
import Toast from './components/Toast';

function App() {
  return (
    <>
      <Router>
        <Route path="/" component={Home} />
        <Route path="/expenses" component={Dashboard} />
        <Route path="/expenses/transactions" component={Transactions} />
        <Route path="/expenses/categories" component={Categories} />
        <Route path="/expenses/ongoing" component={OngoingExpenses} />
        <Route path="/expenses/installments" component={InstallmentExpenses} />
        <Route path="/expenses/monthly-notes" component={MonthlyNotes} />
      </Router>
      <Toast />
    </>
  );
}

export default App;
