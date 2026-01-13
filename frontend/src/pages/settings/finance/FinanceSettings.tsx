import { Navigate } from '@solidjs/router';

const FinanceSettings = () => {
  // Redirect to Categories by default
  return <Navigate href="/settings/finance/categories" />;
};

export default FinanceSettings;

