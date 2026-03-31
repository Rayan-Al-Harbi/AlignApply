from prometheus_client import Counter, Histogram, Gauge

# --- RED: Rate ---
REQUEST_COUNT = Counter(
    "applycheck_requests_total",
    "Total API requests",
    ["endpoint", "status"],  # labels for filtering
)

LLM_CALL_COUNT = Counter(
    "applycheck_llm_calls_total",
    "Total LLM API calls",
    ["agent", "model"],
)

# --- RED: Errors ---
LLM_ERROR_COUNT = Counter(
    "applycheck_llm_errors_total",
    "LLM call failures (timeouts, invalid JSON, API errors)",
    ["agent", "error_type"],
)

PIPELINE_ERROR_COUNT = Counter(
    "applycheck_pipeline_errors_total",
    "Pipeline-level failures",
    ["agent"],
)

# --- RED: Duration ---
REQUEST_LATENCY = Histogram(
    "applycheck_request_duration_seconds",
    "End-to-end request latency",
    ["endpoint"],
    buckets=[1, 5, 10, 20, 30, 45, 60, 90, 120],
)

AGENT_LATENCY = Histogram(
    "applycheck_agent_duration_seconds",
    "Per-agent execution time",
    ["agent"],
    buckets=[0.5, 1, 2, 5, 10, 15, 20, 30],
)

LLM_LATENCY = Histogram(
    "applycheck_llm_call_duration_seconds",
    "Individual LLM call latency",
    ["agent", "model"],
    buckets=[0.5, 1, 2, 3, 5, 8, 10, 15],
)

# --- AI-specific ---
SCORE_DISTRIBUTION = Histogram(
    "applycheck_overall_score",
    "Distribution of overall application scores",
    buckets=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
)

SKILLS_MATCHED = Histogram(
    "applycheck_skills_matched_ratio",
    "Ratio of matched skills to total required skills",
    buckets=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
)