# Python Code Review Guidelines

These guidelines apply to all Python projects in this repository. Every pull request must be reviewed against these criteria before approval.

---

## Severity Definitions

| Tag | Meaning | PR Impact |
|-----|---------|-----------|
| **`[CRITICAL]`** | Security vulnerability, data loss risk, or production outage risk | PR must be **blocked** until fixed |
| **`[HIGH]`** | Bugs causing runtime failures, resource leaks, deployment instability, or dependency hygiene violations | PR requires **changes** before merge |
| **`[MEDIUM]`** | Performance issues, missing validation, DRY violations, weak error handling | PR should be fixed; merge at reviewer discretion if timeline-critical |
| **`[LOW]`** | Style, naming, cosmetic issues | Fix preferred but non-blocking |

---

## 1. Correctness & Security

### Resource Management
- **`[HIGH]`** All file, database connection, socket, and network resource access must use context managers (`with` statements). Never rely on manual `.close()` calls.
- **`[MEDIUM]`** Mutable default arguments are prohibited. Use `None` as the default and initialize inside the function body:
  ```python
  # Wrong
  def f(items=[]):
      ...

  # Correct
  def f(items=None):
      items = items or []
  ```

### Error Handling
- **`[HIGH]`** Every `except` block must either handle, re-raise, or log the exception with stack trace context. Silent swallowing (`except: pass`) is prohibited.
- **`[CRITICAL]`** Error messages returned to callers or written to logs must not contain passwords, tokens, API keys, PII, or internal infrastructure details (hostnames, IPs, internal URLs).
- **`[MEDIUM]`** Use custom exception classes when the caller needs to distinguish between different failure modes.

### Secrets & Credentials
- **`[CRITICAL]`** No secrets, credentials, API keys, or tokens may appear as literals anywhere in source code or committed configuration files (including `.env` files checked into version control).
- **`[CRITICAL]`** All secrets must be injected via environment variables or a secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager).
- **`[CRITICAL]`** The prohibition covers every form a credential can take, not just a variable named `password`. Flag all of the following:
  - String literals assigned to names containing `password`, `passwd`, `pwd`, `secret`, `token`, `api_key`, `apikey`, `access_key`, `client_secret`, `auth`, or `credential`.
  - Credentials embedded in URLs or connection strings: `https://user:pass@host/...`, `postgresql://admin:P%40ss@db:5432/app`, SFTP/FTP URLs with inline passwords, Azure SAS tokens, and JDBC/ODBC connection strings with `PWD=`.
  - Literal `Authorization` header values: `headers={"Authorization": "Bearer eyJhbGci..."}` or a hardcoded Basic auth base64 blob.
  - Private keys and keystores committed to the repository (`.pem`, `.key`, `.p12`, `.pfx`, `id_rsa`, service-account JSON).
  - Credentials in committed config files of any format — `config.ini`, `config.json`, `settings.py`, `application.yml`, `appsettings.json`, Dockerfiles, CI pipeline definitions, and Kubernetes manifests.
- **`[CRITICAL]`** A secret must never have a hardcoded fallback default. `os.getenv("API_KEY", "dev-key-123")` is a hardcoded credential — the default ships to production and silently works until it doesn't. Missing secrets must fail loudly at startup:
  ```python
  # Wrong — the fallback is a committed credential
  API_KEY = os.getenv("API_KEY", "dev-key-123")

  # Correct — fail fast on a missing secret
  API_KEY = os.environ["API_KEY"]  # raises KeyError at startup
  ```
- **`[HIGH]`** Commented-out or placeholder credentials are still violations. `# password = "Prod@2024"` and test/UAT credentials left in the file must be removed — they are real credentials for a real environment.
- **`[HIGH]`** `.env` files must be listed in `.gitignore` and must never be committed. Commit a `.env.example` containing only keys with empty or obviously fake values to document the required configuration.
- **`[CRITICAL]`** Deleting a committed secret from the working tree does not remediate it. The value remains in git history and must be treated as compromised: rotate the credential at its source, then remove it from the code. A PR that only deletes the literal without rotation is not a fix.

### Transport Security
- **`[CRITICAL]`** TLS certificate verification must never be disabled. `verify=False` (requests/httpx), `ssl=False` (aiohttp), `ssl._create_unverified_context()`, and assigning `ssl._create_default_https_context = ssl._create_unverified_context` are all prohibited. Disabling verification means any party on the network path can present a self-signed certificate and silently intercept or modify the traffic, including credentials — the connection is still encrypted, but to an attacker.
- **`[HIGH]`** Suppressing the resulting warning (`urllib3.disable_warnings()`, `InsecureRequestWarning` filters) is prohibited. It hides the defect rather than fixing it.
- **`[HIGH]`** For internal services using a private CA or self-signed certificate, supply the trust anchor instead of disabling verification:
  ```python
  # Wrong
  requests.get(url, verify=False, timeout=3)

  # Correct — trust the internal CA explicitly
  requests.get(url, verify="/etc/ssl/certs/internal-ca.pem", timeout=3)
  ```
  The CA bundle path must come from configuration (e.g., `REQUESTS_CA_BUNDLE` or an env var), not be hardcoded.

### Injection Prevention
- **`[CRITICAL]`** All SQL queries must use parameterized queries or ORM methods. String concatenation, f-strings, or `%` formatting to build SQL is prohibited.
- **`[CRITICAL]`** All external input (API request bodies, query params, headers, file uploads, CLI args) must be validated and sanitized at the trust boundary before use.
- **`[CRITICAL]`** `eval()`, `exec()`, and `pickle.loads()` must never be called on data originating from external or untrusted sources.
- **`[CRITICAL]`** `yaml.load()` must always specify `Loader=yaml.SafeLoader`. Bare `yaml.load(data)` is prohibited.

### Path & Process Safety
- **`[CRITICAL]`** File path operations that accept external input must validate against path traversal (e.g., reject `..` components, resolve and check the canonical path stays within an allowed directory).
- **`[CRITICAL]`** `subprocess` calls must not use `shell=True`. Pass arguments as a list, and never construct command arguments from unsanitized user input.
- **`[HIGH]`** Prefer in-memory processing over the download-save-read-delete pattern. If file content from an HTTP request payload, API response, or any external source is processed and the temporary file is deleted before returning a response, the disk round-trip is pure overhead — the data ends up in memory (e.g., as a DataFrame) regardless. Use `io.BytesIO` / `io.StringIO` to process directly from bytes:
  ```python
  from io import BytesIO
  import pandas as pd

  contents = await file.read()
  df = pd.read_excel(BytesIO(contents))
  ```
  Reserve disk writes only when the processing library strictly requires a filesystem path and has no stream/buffer API.
- **`[HIGH]`** Files obtained from external sources (email attachments, HTTP responses, SFTP downloads, API payloads, user uploads) that must be written to disk must never be saved to the source code directory or the application's working directory. Use `tempfile.mkdtemp()` or `tempfile.NamedTemporaryFile()` to write to OS-managed temporary directories, and clean up after processing:
  ```python
  import tempfile, os

  with tempfile.TemporaryDirectory() as tmp_dir:
      file_path = os.path.join(tmp_dir, filename)
      # write and process file here
  # directory and contents are automatically deleted
  ```

### Authentication & Authorization
- **`[CRITICAL]`** Every protected endpoint or operation must enforce authentication and authorization checks. These checks must not be bypassable through parameter manipulation, header injection, or alternate code paths.

### Concurrency Safety
- **`[HIGH]`** Shared mutable state in concurrent code (threads, async tasks, multiprocessing) must be protected with appropriate synchronization primitives (locks, queues, thread-safe data structures).
- **`[HIGH]`** All I/O inside `async def` functions must be non-blocking and awaited. Synchronous blocking calls block the entire event loop, stalling all concurrent requests. Common violations include:
  - **`[HIGH]`** **HTTP calls**: `requests.get()`, `urllib.request.urlopen()` — use `httpx.AsyncClient` or `aiohttp` instead.
  - **`[HIGH]`** **Database**: synchronous DB drivers (`psycopg2`, `pymysql`, `cx_Oracle`, `pymongo`) — use async drivers (`asyncpg`, `aiomysql`, `motor`) or wrap with `run_in_executor()`.
  - **`[HIGH]`** **File I/O**: `open()`, `pathlib.Path.read_text()`, `shutil` operations — use `aiofiles` or offload to a thread via `asyncio.to_thread()`.
  - **`[HIGH]`** **Sleep**: `time.sleep()` — use `await asyncio.sleep()`.
  - **`[HIGH]`** **Subprocess**: `subprocess.run()`, `subprocess.Popen()` — use `asyncio.create_subprocess_exec()`.
  - **`[HIGH]`** **DNS / socket**: `socket.getaddrinfo()`, `socket.connect()` — use `asyncio.open_connection()` or async DNS resolvers.
  - **`[MEDIUM]`** **OS operations**: `os.listdir()`, `os.stat()`, `os.makedirs()` — offload to `asyncio.to_thread()` if called on slow filesystems (NFS, mounted volumes).

### HTTP Client Timeouts
- **`[HIGH]`** All outbound HTTP requests must specify an explicit timeout. Calls without a timeout can hang indefinitely, holding connections, threads, or async tasks open and eventually exhausting resources.
  - **In API/web request handlers** (FastAPI routes, Flask views, Django views): timeout must not exceed **3 seconds**. An upstream call that takes longer will cascade latency to the end user and risk exhausting the worker pool.
  - **In background tasks** (Celery workers, APScheduler jobs, FastAPI background tasks) and **batch scripts/cron jobs**: timeout must not exceed **30 seconds**, since these do not block HTTP request/response cycles.
  ```python
  # API app — 3s timeout
  requests.get(url, timeout=3)
  async with httpx.AsyncClient(timeout=3) as client: ...

  # Batch/cron — 30s timeout
  requests.get(url, timeout=30)
  ```

### Date & Time Handling
- **`[HIGH]`** `datetime.utcnow()` and `datetime.utcfromtimestamp()` are prohibited. They are deprecated as of Python 3.12 and emit a `DeprecationWarning` on 3.13, but the deprecation is not the real problem — both return a **naive** `datetime` (no `tzinfo`) whose value represents UTC. That object lies about itself, and Python then treats it as local time in every subsequent operation. Since the deployment sets `ENV TZ=Asia/Kolkata`, `.timestamp()` on such a value silently shifts it by 5 hours 30 minutes, and comparing it against a timezone-aware datetime raises `TypeError: can't compare offset-naive and offset-aware datetimes`.
  ```python
  from datetime import datetime, timezone

  # Wrong — deprecated, and naive despite holding a UTC value
  now = datetime.utcnow()
  ts = datetime.utcfromtimestamp(epoch)

  # Correct — timezone-aware UTC
  now = datetime.now(timezone.utc)
  ts = datetime.fromtimestamp(epoch, tz=timezone.utc)
  ```

---

## 2. Code Quality & Style

### Standards
- **`[LOW]`** All code must follow PEP 8 (naming, line length, whitespace, imports).
- **`[LOW]`** Naming conventions: `snake_case` for functions, methods, and variables; `PascalCase` for classes; `UPPER_SNAKE_CASE` for module-level constants.

### Entry-Point Naming
- **`[MEDIUM]`** The application's entry-point module must be named after the project or application it runs — not a generic placeholder. `main.py`, `app.py`, `run.py`, `start.py`, `mainflow.py`, `process.py`, `script.py`, and `test.py` are prohibited as entry-point filenames.

  A Python process identifies itself in `ps`, `top`, `htop`, `py-spy`, container runtime metrics, and APM process listings by its command line. When a dozen pods across a node all report `python main.py`, a CPU or memory spike cannot be attributed to an application without cross-referencing container IDs — which is exactly the moment when that lookup is most expensive. A descriptive name makes the process self-identifying:
  ```
  # Wrong — indistinguishable from every other Python workload on the node
  python main.py
  python mainflow.py

  # Correct — the offending application is obvious from `top` alone
  python life_bulk_pdf_api.py
  python policy_renewal_poller.py
  ```
- **`[MEDIUM]`** The same applies to the module path in a gunicorn `CMD`. Use `life_bulk_pdf_api:app`, not `main:app` or `app:app` — the module name appears in the master and worker command lines.
- **`[LOW]`** The entry-point name should mirror the repository or deployment name in `snake_case` so that process listings, log output, alerts, and dashboards all correlate to the same identifier without translation.

### Cleanliness
- **`[HIGH]`** No dead code, commented-out code blocks, or unused imports/variables may be merged. Remove them before submitting the PR.
- **`[HIGH]`** `print()` statements are prohibited in all code. They bypass log-level control, lack timestamps and context, and fill stdout buffers in long-running processes (causing memory pressure in containerized deployments). Use the `logging` module instead. No exceptions.
- **`[MEDIUM]`** Every function and method must have a single, clear responsibility. If a function does more than one distinct thing, split it.
- **`[MEDIUM]`** No function may exceed 100 lines. Any class exceeding 300 lines should be flagged for refactoring discussion.
- **`[LOW]`** Variable and function names must be descriptive of their purpose. Single-letter names (`x`, `d`) are acceptable only in trivial lambdas, comprehensions, or well-known mathematical contexts. Names like `temp`, `data2`, `result1` are prohibited.

---

## 3. Structure & Design

- **`[MEDIUM]`** Duplicated logic must be extracted into shared functions or modules (DRY). If the same logic appears in three or more places, refactor it. Two occurrences may be acceptable if they are likely to diverge independently.
- **`[LOW]`** Use classes when you need shared state across methods; use standalone functions for stateless operations; use modules to group related functionality.
- **`[HIGH]`** Circular imports are prohibited. Restructure modules or use lazy imports to break cycles.
- **`[MEDIUM]`** No magic numbers or magic strings in business logic. Extract them as named constants or externalized configuration values.

### Global Variable Usage
- **`[HIGH]`** Mutable global state is prohibited. Do not use module-level mutable variables (`list`, `dict`, `set`, or class instances) as shared state across functions. Mutable globals create hidden coupling, make testing difficult, and cause inconsistent behavior in multi-worker deployments (each gunicorn worker gets its own copy).
- **`[MEDIUM]`** Module-level constants are acceptable but must be immutable and named in `UPPER_SNAKE_CASE`. Use `tuple` or `frozenset` instead of `list` or `set` for constant collections:
  ```python
  # Wrong
  SUPPORTED_FORMATS = ["pdf", "xlsx"]

  # Correct
  SUPPORTED_FORMATS = frozenset({"pdf", "xlsx"})
  MAX_RETRIES = 3
  ```
- **`[HIGH]`** Configuration values must not be stored as mutable globals. Load config from environment variables or config files at startup and pass via dependency injection, function parameters, or a config object — not by mutating a global dict that other modules import.
- **`[HIGH]`** In-process global caches (`dict`, `@lru_cache`, etc.) are prohibited in API/web applications. Each gunicorn worker holds its own copy, leading to inconsistent data across workers, unbounded memory growth, and stale entries with no eviction. Use an external cache (Redis, Memcached) instead. In batch scripts and standalone processes, bounded caches (`@functools.lru_cache(maxsize=N)`, `cachetools.TTLCache`) are acceptable if justified.
- **`[MEDIUM]`** No function should modify a global variable as a side effect. If a function body contains `global x` or `module.x = ...`, refactor to return values or accept parameters instead.

---

## 4. Performance

- **`[MEDIUM]`** Avoid N+1 query patterns: do not issue a database or API call inside a loop when a single batch query would suffice.
- **`[MEDIUM]`** Prefer `set` or `dict` for membership checks and lookups. `list` has O(n) lookup time, so when the same collection is checked repeatedly (e.g., inside a loop or called per request), use a `set` or `dict` regardless of size.
- **`[LOW]`** Avoid copying large data structures unnecessarily. Prefer in-place operations or views where safe.
- **`[MEDIUM]`** For large datasets, use generators or iterators instead of materializing everything into memory at once.
- **`[MEDIUM]`** Do not perform repeated expensive computations (DB calls, API calls, heavy calculations) inside loops — hoist them above the loop or cache results.
- **`[MEDIUM]`** Flag algorithms with O(n²) or worse complexity on potentially large inputs: nested loops over the same collection, repeated linear searches in lists, and string concatenation via `+=` in a loop (use `"".join(parts)` or list-append-then-join instead).
- **`[HIGH]`** No synchronous blocking calls in async code paths (see Section 1, Concurrency Safety).

### Pandas Performance
- **`[HIGH]`** Do not iterate over DataFrame rows using `iterrows()`, `itertuples()`, or `for i in range(len(df))` when a vectorized operation or `.apply()` would work. Row-by-row iteration is orders of magnitude slower.
- **`[HIGH]`** Do not build a DataFrame by appending rows in a loop (`pd.concat()` or `df.append()` inside a loop). Collect rows in a list and call `pd.concat()` once after the loop.
- **`[MEDIUM]`** Do not use `.apply()` when a vectorized equivalent exists — e.g., `df['col'].apply(lambda x: x.upper())` should be `df['col'].str.upper()`. The same applies to arithmetic, comparison, and string operations that pandas supports natively.
- **`[MEDIUM]`** Specify `dtype` and `usecols` when calling `pd.read_csv()` / `pd.read_excel()`. Omitting `dtype` forces pandas to infer types (slow, memory-heavy). Omitting `usecols` loads columns that may never be used.
- **`[MEDIUM]`** Use `category` dtype for low-cardinality string columns (e.g., status codes, country names). Object dtype stores each value as a separate Python string, consuming significantly more memory.
- **`[MEDIUM]`** Use built-in GroupBy aggregations (`.sum()`, `.mean()`, `.agg()`) instead of `.groupby().apply(lambda ...)` for standard aggregations. `.apply()` falls back to row-by-row execution.
- **`[MEDIUM]`** Filter DataFrames as early as possible. Apply row filters before performing transformations, joins, or aggregations to reduce the working set.
- **`[MEDIUM]`** Use `regex=False` in `.str.contains()`, `.str.replace()`, and similar methods when matching literal strings. The default compiles a regex engine per call.
- **`[MEDIUM]`** Use `.loc[mask, col]` instead of chained indexing (`df[col][mask]`). Chained indexing is slower and risks `SettingWithCopyWarning`.
- **`[LOW]`** Set the join key as the index (`.set_index()`) before merging large DataFrames when the same key is used for multiple joins.
- **`[LOW]`** Avoid unnecessary `.reset_index()` and `.copy()` calls that create full DataFrame copies with no functional benefit.

---

## 5. Dependencies & Environment

- **`[LOW]`** Every new dependency must be justified in the PR description (why it's needed and what alternatives were considered).
- **`[HIGH]`** All dependencies used in the code must be listed in `requirements.txt` (or `pyproject.toml`) with pinned versions (e.g., `fastapi==0.115.0`, not `fastapi` or `fastapi>=0.100`). This applies to deployable applications; library projects (maintained in separate repositories) should use version ranges.
- **`[HIGH]`** No unused dependencies may remain in `requirements.txt`. Remove them when the code that required them is deleted.
- **`[HIGH]`** A dependency is not considered "used" merely because it has an `import` statement. The imported module, class, or function must be actively referenced in application logic (called, passed, configured, or otherwise utilized). A bare `import foo` with no subsequent reference to `foo` anywhere in the codebase is dead code and the dependency must be removed from `requirements.txt`. Exception: libraries that activate purely via import-time side effects (e.g., `autodynatrace` for APM instrumentation) must include a comment at the import site explaining the side-effect purpose:
  ```python
  import autodynatrace  # noqa: F401 — activates Dynatrace instrumentation on import
  ```
- **`[HIGH]`** All dependencies must be compatible with the project's Python version (currently 3.13).

---

## 6. Logging & Observability

- **`[HIGH]`** All application logging must use Python's `logging` module (or a structured logging library like `structlog`).
- **`[MEDIUM]`** Every module must obtain a logger via `logger = logging.getLogger(__name__)`. Do not use the root logger directly.
- **`[MEDIUM]`** A logging configuration (format, handler, level) must be set up at application startup — either via `logging.basicConfig()`, `logging.config.dictConfig()`, or framework-provided config. Logs must include at minimum: timestamp, log level, module/logger name, and message.
- **`[LOW]`** Use appropriate log levels:
  - `DEBUG` — verbose diagnostic info, disabled in production.
  - `INFO` — routine operational events (startup, request served, job completed).
  - `WARNING` — unexpected but recoverable situations.
  - `ERROR` — failures that need attention (with stack traces via `logger.exception()` or `exc_info=True`).
- **`[HIGH]`** Exceptions must be logged with sufficient context (what operation failed, relevant identifiers) and stack trace before being re-raised or handled. Use `logger.exception()` inside `except` blocks (automatically attaches traceback) or `logger.error("...", exc_info=True)`.
---

## 7. API / Interface Design

- **`[MEDIUM]`** All API endpoints must validate request input (types, required fields, value ranges) and return clear error responses with appropriate HTTP status codes.
- **`[MEDIUM]`** Response formats must be consistent across the application (uniform envelope structure, consistent error schema).
- **`[LOW]`** API versioning strategy must be followed if the project defines one.

---

## 8. Configuration & Deployment

- **`[HIGH]`** Environment-specific values must be externalized via environment variables or config files — never hardcoded in source. This covers:
  - **URLs and endpoints** — upstream API base URLs, webhook targets, callback URLs, health-check targets.
  - **Hosts, IPs, and ports** — database hosts, SFTP/FTP servers, SMTP servers, message brokers, proxy addresses, and any literal IP address.
  - **Filesystem and share paths** — network shares (`\\fileserver\reports`), mount points, and absolute local paths (`D:\data\input`, `/home/user/files`).
  - **Email addresses** — sender addresses, recipient lists, distribution groups, and escalation contacts.
  - **Identifiers and tunables** — account numbers, tenant IDs, queue and topic names
  ```python
  # Wrong — changing environment requires a code change and redeploy
  BASE_URL = "https://uat-api.internal.example.com/v1"
  resp = requests.get(f"{BASE_URL}/policy/{policy_id}", timeout=3)

  # Correct — supplied per environment
  BASE_URL = os.environ["POLICY_API_BASE_URL"]
  resp = requests.get(f"{BASE_URL}/policy/{policy_id}", timeout=3)
  ```
- **`[HIGH]`** Code must not branch on the environment name to select configuration. `if env == "prod": url = ... else: url = ...` embeds every environment's topology in the source and breaks the moment a new environment is added. Supply the value itself, not the rule for choosing it.
- **`[HIGH]`** Configuration defaults must never point at a production or shared resource. A default is acceptable only for a genuinely environment-independent tunable (`BATCH_SIZE`, `LOG_LEVEL`); hosts, URLs, and paths must be explicitly provided. See also the prohibition on fallback credentials in Section 1.
- **`[HIGH]`** Dependencies must be pinned in `requirements.txt` or `pyproject.toml` (see Section 5).
- **`[HIGH]`** Applications must not store stateful data in-memory or on the local filesystem in a way that assumes a single instance. In-memory caches, session stores, counters, file-based locks, and locally written temp files will not be shared across pods and will cause inconsistent behavior when the service scales horizontally. Use external stores (Redis, database, shared object storage) for any state that must be consistent across instances.

### Graceful Shutdown (Non-API Applications)

> **Applicability**: This subsection applies to all long-running Python processes that are **not** HTTP APIs (batch processors, polling loops, background workers, scheduled-task runners). API applications already get graceful shutdown from gunicorn's signal handling.

- **`[HIGH]`** All non-API long-running processes must handle `SIGTERM` and `SIGINT` for graceful shutdown. Kubernetes sends `SIGTERM` before killing a pod — processes that ignore it are force-killed mid-operation, risking data corruption, partial writes, and orphaned locks. The implementation must:
  1. Register signal handlers for `SIGTERM` and `SIGINT`.
  2. Use a shared `threading.Event` (or equivalent) to signal all loops and threads to stop.
  3. Allow in-flight work (current iteration, active batch) to complete before exiting.
  4. Log shutdown initiation and completion.
  ```python
  import signal
  import threading

  shutdown_event = threading.Event()

  def _signal_handler(signum, _frame):
      logger.info("Received signal %s, initiating graceful shutdown...", signum)
      shutdown_event.set()

  signal.signal(signal.SIGTERM, _signal_handler)
  signal.signal(signal.SIGINT, _signal_handler)

  while not shutdown_event.is_set():
      process_next_batch()

  logger.info("Processing loop exited cleanly.")
  ```
- **`[HIGH]`** Sleep-based polling loops must check the shutdown event instead of using bare `time.sleep()`. Use `shutdown_event.wait(timeout)` so the process can wake immediately on signal rather than sleeping through the remaining interval. `shutdown_event.wait(timeout=N)` blocks for up to N seconds but returns `True` immediately if the event is set — making the process responsive to SIGTERM within milliseconds instead of waiting out the full interval:
  ```python
  # Wrong — blocks for the full 120s even after SIGTERM.
  # If Kubernetes terminationGracePeriodSeconds is 30s, the process
  # will be SIGKILL'd mid-sleep, leaving work in an unknown state.
  while not shutdown_event.is_set():
      process_pending_records()
      logger.info("Sleeping %s seconds before next poll...", POLL_INTERVAL)
      time.sleep(POLL_INTERVAL)  # <-- deaf to signals

  # Correct — returns immediately when shutdown_event is set.
  # The loop exits cleanly within the grace period.
  while not shutdown_event.is_set():
      process_pending_records()
      logger.info("Sleeping %s seconds before next poll...", POLL_INTERVAL)
      shutdown_event.wait(timeout=POLL_INTERVAL)

  logger.info("Polling loop exited cleanly.")
  ```
  This applies to every `time.sleep()` in the process — including retry delays, rate-limit backoffs, and inter-batch pauses. Replace all of them with `shutdown_event.wait(timeout=N)`.

- **`[MEDIUM]`** Background threads spawned by the main process must also respect the shutdown event. Pass the event to thread targets and check it in their loops. Use `daemon=True` for threads that should not prevent process exit. A thread that ignores the event will either block shutdown or be killed abruptly by the OS when the main thread exits:
  ```python
  import threading

  def run_mailer_loop(shutdown_event):
      """Send pending notification emails on a fixed interval."""
      while not shutdown_event.is_set():
          try:
              send_pending_mails()
          except Exception as err:
              logger.exception("Mailer loop failed - %s", err)
          shutdown_event.wait(timeout=60)
      logger.info("Mailer loop exited cleanly.")

  def run_cleanup_loop(shutdown_event):
      """Purge stale temp files every 5 minutes."""
      while not shutdown_event.is_set():
          try:
              purge_stale_files()
          except Exception as err:
              logger.exception("Cleanup loop failed - %s", err)
          shutdown_event.wait(timeout=300)
      logger.info("Cleanup loop exited cleanly.")

  # Main entry point — spawn threads and run primary loop
  if __name__ == "__main__":
      shutdown_event = threading.Event()
      signal.signal(signal.SIGTERM, lambda sig, _: shutdown_event.set())
      signal.signal(signal.SIGINT, lambda sig, _: shutdown_event.set())

      threading.Thread(
          target=run_mailer_loop, args=(shutdown_event,), daemon=True
      ).start()
      threading.Thread(
          target=run_cleanup_loop, args=(shutdown_event,), daemon=True
      ).start()

      # Primary processing loop (blocks until shutdown)
      while not shutdown_event.is_set():
          process_next_batch()
          shutdown_event.wait(timeout=120)

      logger.info("All loops exited. Process shutting down.")
  ```
  Key requirements for background threads:
  - Accept `shutdown_event` as a parameter (not a global import).
  - Use `shutdown_event.is_set()` as the loop condition.
  - Use `shutdown_event.wait(timeout=N)` instead of `time.sleep(N)` for all pauses.
  - Mark as `daemon=True` so the process can exit even if a thread is stuck in an uninterruptible call.

---

## 9. Dockerfile Standards

### Base Image
- **`[MEDIUM]`** Use `python:3.13-slim-bookworm` (or the current project-standard slim variant). Do not use `alpine` unless there is a documented reason. Do not use full/untagged images.

### ASGI/WSGI Server Requirement

> **Applicability**: This subsection applies only to Dockerfiles that serve an API (FastAPI, Flask, Django, etc.). Batch scripts, cron jobs, and standalone Python processes that do not expose HTTP endpoints are exempt from gunicorn/uvicorn requirements — they should use `CMD ["python", "<application_name>.py"]` directly, where the filename follows the entry-point naming rule in Section 2.

- **`[HIGH]`** Every Dockerfile serving an API must use a production-grade ASGI/WSGI server. Running the application with bare `python app.py` or `flask run` in production is prohibited.
- **`[HIGH]`** Using `uvicorn` directly as the process manager (e.g., `uvicorn app:app --workers N`) is prohibited. Uvicorn lacks robust process management — no automatic worker restart on crashes or memory leaks, no graceful reload, and no worker-level timeout enforcement.
- **`[HIGH]`** **For FastAPI / Starlette (ASGI) apps**, use Gunicorn with UvicornWorker. The `uvicorn[standard]` package includes `uvloop` and `httptools` automatically, so the event loop performance is identical to running uvicorn directly:
  ```dockerfile
  CMD ["gunicorn", "app_module:app", \
       "--workers", "2", \
       "--worker-class", "uvicorn.workers.UvicornWorker", \
       "--bind", "0.0.0.0:<PORT>", \
       "--timeout", "30", \
       "--graceful-timeout", "30", \
       "--max-requests", "5000", \
       "--max-requests-jitter", "500", \
       "--access-logfile", "-"]
  ```
- **`[HIGH]`** **For Flask / Django (WSGI) apps**, use Gunicorn directly:
  ```dockerfile
  CMD ["gunicorn", "app_module:app", \
       "--workers", "2", \
       "--bind", "0.0.0.0:<PORT>", \
       "--timeout", "30", \
       "--graceful-timeout", "30", \
       "--max-requests", "5000", \
       "--max-requests-jitter", "500", \
       "--access-logfile", "-"]
  ```

### CMD Exec Form
- **`[HIGH]`** `CMD` must always use exec form (`CMD ["executable", "arg1", "arg2"]`), never shell form (`CMD executable arg1 arg2`). Shell form wraps the command in `/bin/sh -c`, so the actual process runs as a child of the shell — not as PID 1. Kubernetes sends `SIGTERM` to PID 1 during pod shutdown, and `/bin/sh` does not forward signals to child processes. This means the application never receives `SIGTERM`, never performs graceful shutdown, and is force-killed by `SIGKILL` after `terminationGracePeriodSeconds`.

### Mandatory Gunicorn Arguments

Every gunicorn CMD **must** include all of the following arguments. Omitting any is a `[HIGH]` violation:

| Argument | Purpose | Required Value |
|----------|---------|----------------|
| `--workers <N>` | Number of worker processes | 2–4 workers. Use env var for flexibility: `--workers ${WORKERS:-2}`. Scaling is handled at the pod level via Kubernetes — do not over-allocate workers per container |
| `--worker-class uvicorn.workers.UvicornWorker` | ASGI worker (FastAPI/Starlette only) | Always use this exact value for ASGI apps. Omit for Flask/Django WSGI apps |
| `--bind 0.0.0.0:<PORT>` | Listen address and port | Use the port required by the project's deployment config |
| `--timeout 30` | Kill and restart a worker if it's silent for this long | 30 seconds. Deviations must be justified in the PR description (e.g., bulk/report endpoints requiring longer processing) |
| `--graceful-timeout 30` | Time to wait for in-flight requests to finish after SIGTERM before force-killing the worker | 30 seconds |
| `--max-requests 5000` | Restart worker after serving this many requests | 5000. Prevents memory leaks from accumulating |
| `--max-requests-jitter 500` | Randomize restart to avoid all workers restarting simultaneously | 500 (10% of `--max-requests`) |
| `--access-logfile -` | Write access logs to stdout | Always use `-` (stdout) so container log drivers capture them |
- **`[HIGH]`** Required dependencies in `requirements.txt` (pinned versions):
  ```
  gunicorn==23.0.0
  uvicorn[standard]==0.34.0
  ```
  The `[standard]` extra installs `uvloop`, `httptools`, and `websockets` — do not add them as separate dependencies.

### Server Configuration Rules
- **`[HIGH]`** For ASGI apps, `uvloop` must be available at runtime for optimal event loop performance. The `uvicorn[standard]` dependency already installs `uvloop`, and UvicornWorker automatically selects it when present — no explicit `--loop` flag or `ENV UVICORN_LOOP` is needed. Do **not** pass `--loop uvloop` to uvicorn or set `ENV UVICORN_LOOP=uvloop` in the Dockerfile — this raises a runtime exception in current uvicorn versions. Simply ensure `uvicorn[standard]` is in `requirements.txt` and uvloop will be used automatically.
- **`[HIGH]`** `--reload` flag is prohibited in Dockerfiles. It is a development-only feature and causes unnecessary file-system watching overhead and potential instability in production.
- **`[HIGH]`** All mandatory arguments listed in the table above must be present in the CMD. Missing any argument is a `[HIGH]` violation.

### Non-Root User Configuration
- **`[CRITICAL]`** The application must run as a non-root user. A dedicated user must be created and activated before the `CMD` instruction. Dockerfiles that omit `USER` or leave it as `root` are a `[CRITICAL]` violation.
- **`[HIGH]`** The `USER` instruction must appear **after** all `RUN` commands that require root privileges (package installs, directory creation, file permission changes) and **before** `CMD`/`ENTRYPOINT`.
- **`[HIGH]`** The application directory and any files the app needs to write to at runtime must be owned by the non-root user. Use `chown` in the same layer that creates the directory:
  ```dockerfile
  RUN useradd --create-home appuser \
      && mkdir -p /app/logs \
      && chown -R appuser:appuser /app
  WORKDIR /app
  COPY --chown=appuser:appuser . .
  USER appuser
  CMD ["gunicorn", "app_module:app", ...]
  ```
- **`[MEDIUM]`** The non-root user must not have a login shell or password configured. Use `--no-log-init --shell /usr/sbin/nologin` if the image doesn't need interactive access:
  ```dockerfile
  RUN useradd --no-log-init --create-home --shell /usr/sbin/nologin appuser
  ```
- **`[HIGH]`** Do not grant `sudo` access to the non-root user. If a Dockerfile installs `sudo` and adds the app user to the sudoers group, it defeats the purpose of running as non-root.

### General Dockerfile Best Practices
- **`[LOW]`** Set timezone explicitly if the application depends on local time:
  ```dockerfile
  ENV TZ=Asia/Kolkata
  ```
- **`[LOW]`** Use `--no-cache-dir` with pip installs to reduce image size.
- **`[MEDIUM]`** Clean up build artifacts, caches, and temporary files (SSH keys, apt caches) in the same `RUN` layer they are created.
- **`[CRITICAL]`** Do not store secrets in Dockerfile `ENV` or `ARG` instructions. Use runtime environment variables or Docker secrets.
- **`[MEDIUM]`** SAS URLs with embedded credentials (e.g., Azure Blob Storage signed URLs) in `RUN` instructions are retained in Docker layer history even if the downloaded file is deleted. Migrate to Docker BuildKit secrets (`--mount=type=secret`) or multi-stage builds to avoid credential exposure in image layers. Until the alternate solution is implemented, ensure the SAS token has the narrowest possible scope (read-only, single blob, short expiry) and the download + cleanup happen in a single `RUN` layer.
- **`[LOW]`** Combine `apt-get update` and `apt-get install` in a single `RUN` layer and clean up with `rm -rf /var/lib/apt/lists/*`.
- **`[LOW]`** Use `.dockerignore` to exclude unnecessary files (`.git`, `__pycache__`, `*.pyc`, `.env`, test fixtures).
