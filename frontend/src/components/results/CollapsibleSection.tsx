import { useState } from "react";

interface Props {
  title: string;
  icon: React.ReactNode;
  defaultOpen?: boolean;
  badge?: React.ReactNode;
  children: React.ReactNode;
}

export default function CollapsibleSection({ title, icon, defaultOpen = false, badge, children }: Props) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className="glass-card rounded-2xl overflow-hidden animate-fade-up">
      <button
        onClick={() => setOpen(!open)}
        className="collapsible-trigger w-full flex items-center justify-between px-5 py-4 transition-colors
                   hover:bg-gray-50/50 dark:hover:bg-gray-700/30"
      >
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gray-100 dark:bg-gray-700/80 flex items-center justify-center text-gray-600 dark:text-gray-300">
            {icon}
          </div>
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white">{title}</h3>
          {badge}
        </div>
        <svg
          className={`w-4 h-4 text-gray-400 dark:text-gray-500 transition-transform duration-200 ${open ? "rotate-180" : ""}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {open && (
        <div className="collapsible-content px-5 pb-5">
          {children}
        </div>
      )}
    </div>
  );
}
