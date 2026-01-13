import { Navigate } from '@solidjs/router';

const Settings = () => {
  // Redirect to Finance settings by default
  return <Navigate href="/settings/finance" />;
};

export default Settings;

