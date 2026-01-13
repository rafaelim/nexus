import { Show } from 'solid-js';
import { useLocation } from '@solidjs/router';
import SidePanel from './SidePanel';
import SettingsSidePanel from '../pages/settings/components/SettingsSidePanel';
import TopBar from './TopBar';

interface LayoutProps {
  children: JSX.Element;
}

const Layout = (props: LayoutProps) => {
  const location = useLocation();
  const isSettingsRoute = () => location.pathname.startsWith('/settings');

  return (
    <div class="min-h-screen bg-gray-50 flex flex-col">
      <TopBar />
      <div class="flex flex-1 pt-16">
        <SidePanel />
        <main class={`flex-1 p-8 ml-64 ${isSettingsRoute() ? 'mr-64' : ''}`}>
          {props.children}
        </main>
        <Show when={isSettingsRoute()}>
          <SettingsSidePanel />
        </Show>
      </div>
    </div>
  );
};

export default Layout;

