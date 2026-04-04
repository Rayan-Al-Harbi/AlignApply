import UploadForm from "./components/upload/UploadForm";
import AnalysisProgress from "./components/loading/AnalysisProgress";
import ResultsDashboard from "./components/results/ResultsDashboard";
import { useAnalysis } from "./hooks/useAnalysis";
import { useDarkMode } from "./hooks/useDarkMode";

export default function App() {
  const {
    phase,
    result,
    error,
    isRescoring,
    disputedSkills,
    submit,
    toggleDispute,
    submitDispute,
    reset,
  } = useAnalysis();

  const { dark, toggle } = useDarkMode();

  return (
    <>
      {/* Animated mesh background */}
      <div className="bg-mesh">
        <div className="grid-overlay" />
        <div className="bg-orb bg-orb-1" />
        <div className="bg-orb bg-orb-2" />
      </div>

      <div className="min-h-screen relative">
        {/* Floating dark mode toggle */}
        <button
          onClick={toggle}
          className="fixed top-5 right-5 z-50 w-10 h-10 rounded-full glass-card flex items-center justify-center
                     text-gray-600 dark:text-gray-300 hover:scale-110 transition-transform"
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

        <main className="max-w-6xl mx-auto px-4 sm:px-6 py-10 sm:py-16">
          {phase === "input" && <UploadForm onSubmit={submit} />}

          {phase === "loading" && <AnalysisProgress />}

          {phase === "results" && result && (
            <ResultsDashboard
              result={result}
              disputedSkills={disputedSkills}
              isRescoring={isRescoring}
              onToggleDispute={toggleDispute}
              onSubmitDispute={submitDispute}
              onStartOver={reset}
            />
          )}

          {phase === "error" && (
            <div className="max-w-md mx-auto text-center py-16 animate-fade-up">
              <div className="w-16 h-16 rounded-2xl bg-danger/10 flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-danger" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                </svg>
              </div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Analysis Failed</h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">{error}</p>
              <button
                onClick={reset}
                className="px-6 py-2.5 rounded-xl bg-primary text-white text-sm font-semibold hover:bg-primary-dark transition-colors"
              >
                Try Again
              </button>
            </div>
          )}
        </main>
      </div>
    </>
  );
}
