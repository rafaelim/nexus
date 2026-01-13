import { Navigate } from '@solidjs/router';

const Settings = () => {
  // Redirect to General settings by default
  return <Navigate href="/settings/general" />;
};

export default Settings;

