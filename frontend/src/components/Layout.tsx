import { createSignal, onMount } from 'solid-js';
import SidePanel from './SidePanel';

interface LayoutProps {
  children: JSX.Element;
}

const Layout = (props: LayoutProps) => {
  return (
    <div class="min-h-screen bg-gray-50 flex">
      <SidePanel />
      <main class="flex-1 p-8 ml-64">
        {props.children}
      </main>
    </div>
  );
};

export default Layout;

