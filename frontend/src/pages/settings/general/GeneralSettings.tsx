import { Navigate } from '@solidjs/router';

const GeneralSettings = () => {
  // Redirect to Properties by default
  return <Navigate href="/settings/general/properties" />;
};

export default GeneralSettings;

