interface Props {
  dark: boolean;
  onToggleDark: () => void;
}

export default function Header({ dark, onToggleDark }: Props) {
  return (
    <header className="glass-card sticky top-0 z-30 border-b border-gray-200/50 dark:border-gray-700/50">
      <div className="max-w-6xl mx-auto px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-br from-primary to-indigo-600 rounded-lg flex items-center justify-center shadow-sm shadow-primary/20">
            <svg className="w-4.5 h-4.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 className="text-lg font-bold text-gray-900 dark:text-white tracking-tight">
            ApplyCheck
          </h1>
        </div>

        <div className="flex items-center gap-4">
          <p className="text-sm text-gray-500 dark:text-gray-400 hidden sm:block">
            AI-Powered Application Analysis
          </p>
          <button
            onClick={onToggleDark}
            className="w-9 h-9 rounded-xl flex items-center justify-center transition-colors
                       bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700
                       text-gray-600 dark:text-gray-300"
            aria-label="Toggle dark mode"
          >
            {dark ? (
              <svg className="w-[18px] h-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            ) : (
              <svg className="w-[18px] h-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
