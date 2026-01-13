const TopBar = () => {
  return (
    <div class="bg-white border-b border-gray-200 h-16 fixed top-0 left-0 right-0 z-50 flex items-center px-8">
      <div class="flex items-center justify-between w-full">
        <h1 class="text-xl font-semibold text-gray-900">Nexus</h1>
        <div class="flex items-center space-x-4">
          {/* Future: Add user menu, notifications, etc. */}
        </div>
      </div>
    </div>
  );
};

export default TopBar;

