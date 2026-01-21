# Jacek's QA Demo Repository

TL;DR: 
Modern, Dockerized, reproducible tests repository with CI, parallelization, and artifacts—ready for your next team!

Hello QA/HR Adventurer!

I’m happy to share this skill-demonstrative repository, which provides a structured and automated framework for 
executing UI and API tests using Python, Playwright, PyTest, and Docker. It supports running tests in parallel, generating
detailed reports, capturing screenshots on test failures, and simplifies configuration management.
The repository includes a changelog, tagged versions, and a robust GitHub Actions CI setup.

My goal is to showcase my experience in building professional, reliable test repositories to accelerate and smoothen the
recruitment process.

This README is intentionally thorough: I like my documentation to be well-structured, informative, and full of 
easy-to-use examples. I’ve added a Detailed Workflow section for a quick grasp of how the repository works.

After more than 5 years as QA Engineer with the Piwik PRO Analytics team, I’ve overcome many challenges and handled
responsibilities that required timely and professional delivery. I worked in an agile process with around 10 developers,
had a lot of freedom of action, and was engaged in idea conception and new solutions at early stages. 
My work split was about 40% manual testing and 60% coding.

Tests you can find in this repository are not meant to show every case that could have been covered by them, but as a showcase
of my approach to building test suite.

If you like what you see — hire me!

Jacek

---

## License

This project is released under a limited-use license. See the [LICENSE](LICENSE) file for details.

---
## Technologies

* **Python 3.12**
* **Playwright**
* **PyTest** (including plugins: `pytest-xdist`, `pytest-html`, `pytest-playwright`, `pytest-rerunfailures`)
* **Docker** & **Docker Compose** (must be installed separately)
* **Poetry** (dependency management)
* **pre-commit** (linters)

---
## Setup

### Prerequisites

Ensure [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed

Verify installations:

```
docker --version
docker compose version
```
---
### 1. Clone the repository

```
git clone https://github.com/gwojacek/playwright-qa-tests.git
cd playwright-qa-tests
```
### 2. Install Poetry (if not installed)
Poetry is required for dependency management. You only need to install it once per machine.

Check if Poetry is already installed:
```
poetry --version

```
If not, then:
```

curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```
For more detailed information and advanced installation options, you can refer to the official Poetry documentation:

[Poetry Installation Guide](https://python-poetry.org/docs/#installing-with-the-official-installer)

---

### 3. Install Python dependencies using Poetry

```
poetry install
```
---
## Configuration

Tests rely on environment-specific configuration files located in the root directory:

* `localconf_local.env`
* `localconf_staging.env`

Create these manually:

```env
# localconf_local.env
ADDRESS="https://www.automationexercise.com/"


# localconf_staging.env
ADDRESS="https://www.automationexercise.com/"

```

The correct file is automatically loaded based on the environment you specify with `-e`.

---
## Executing Tests

The `run_tests.sh` script manages test execution with several customizable options:

* `-b`: Browser selection (`chromium`, `webkit`)
* `-m`: PyTest marker (**required**) (e.g., `ui`, `api`, or other)
* `-n`: Number of parallel workers (specific number, default `auto`)
* `-H`: Disable headless mode (useful for debugging)
* `-D`: Enable Playwright Inspector (PWDEBUG=1, requires `-H`)
* `-T`: Enable Playwright tracing (`--tracing=retain-on-failure`)
* `-e`: Environment type (`local`, `staging`, default `local`)
* `-r`: Number of reruns for failed tests (default `1`)


**Notes:**

* The **`-m` marker is required** to specify which tests to run.
* If you do not provide `-b`, the browser defaults to **chromium**.
* **Headless mode is enabled by default** unless you add `-H`.
* When using Playwright Inspector (`-D`), workers are automatically set to `1`.


## Run Tests Examples

```
# Run UI tests on Chromium (browser defaults to chromium)
./run_tests.sh -m ui

# Run API tests on Webkit with specific environment
./run_tests.sh -b webkit -m api -e staging

# Run UI tests with 4 parallel workers
./run_tests.sh -n 4 -m ui

# Run UI tests in headed mode with Playwright Inspector
./run_tests.sh -m ui -D

# Run UI tests with tracing enabled
./run_tests.sh -m ui -T
```

---
## Debugging

This project provides several tools for debugging failed tests:

1.  **Screenshots:** Automatically captured on failure and saved to `tests/artifacts/`. They are also embedded in the HTML report.
2.  **HTML Report:** A detailed report is generated after each run:
    ```
    -------- Generated html report: file://$(pwd)/tests/artifacts/report.html --------
    ```
3.  **Playwright Tracing:** When enabled with `-T`, traces are saved for failed tests. The script will output commands to view them, for example:
    ```
    npx playwright show-trace tests/artifacts/test_name.zip
    ```
4.  **Playwright Inspector:** Run with `-H -D` to step through tests interactively.
---

## Running Linters

You can execute linters using Poetry  - it runs black, isort and flake8:

```
poetry run lints
```
---

## Commitizen

This repository uses [Commitizen](https://commitizen-tools.github.io/commitizen/) to enforce Conventional Commits and manage release versions. Commit messages are validated via a pre-commit hook.

### Making commits

- add files by `git add .` for all changes or with specified files.

- instead of `git commit`, use:  
`poetry run cz commit`

- fill up questionare form

- `git push`

### Releasing a new version

When you're ready to release:  
`poetry run cz bump`

This command:
- Analyzes commit history
- Updates `pyproject.toml`
- Amends `Changelog.md`
- Creates a Git tag (e.g., `v1.0.1`)

**Important:** Version numbers only change when `poetry run cz bump` is executed, not on every commit.

---


## Test Markers

Markers help categorize tests, making selective execution straightforward during test runs. Example markers defined in
`utils/markers.py`:

```
ui = pytest.mark.ui
api = pytest.mark.api
```

You can create additional markers for your specific testing needs.

---

## Detailed Workflow

### 1. **Starting the Test (`./run_tests.sh ...`)**

* The `run_tests.sh` Bash script is your entrypoint. It parses arguments (browser, marker, workers, headless, environment, etc.).
* It handles environment cleanup and prepares the artifact directory.

---

### 2. **Test Runner Container is Built (Dockerfile)**

* The script calls `docker compose build test-runner` to build the test image:

  1. **FROM mcr.microsoft.com/playwright/python**
     * Uses the official Playwright Python image, which comes pre-installed with all necessary browser dependencies.
  2. **Poetry Install**
     * Installs Poetry and project dependencies.
  3. **Xvfb**
     * Installs `xvfb` to support headed mode inside the container if needed.
  4. **Copy Application Code**
     * Brings all source code, tests, and configs into the container.
* **Result:** A reproducible, isolated test runner container.

---

### 3. **Running Pytest Inside the Container**

* The `docker compose run --rm ... test-runner ...` command starts the container.
* If headed mode (`-H`) is requested, it mounts the X11 socket and sets the `DISPLAY` environment variable.
* `pytest` is invoked with the specified parameters (`--browser`, `-m`, `-n`, `--tracing`, etc.).

---

### 4. **Test Execution, Reporting, and Artifacts**

* Tests run in parallel using `pytest-xdist`.
* **Playwright** launches browsers directly within the container.
* If a test fails:
  * A screenshot is saved to `tests/artifacts/`.
  * If tracing (`-T`) is enabled, a Playwright trace zip file is generated.
* `pytest-html` generates a self-contained HTML report.

---

### 5. **Test Completion and Cleanup**

* After the test run, the script stops the containers and removes orphans.
* It prints summary information and paths to the generated reports and traces.

---

## Bug Tracking

Discovered issues are logged in https://github.com/gwojacek/qa-demo-repository/issues as a showcase of how I handle 
bugs. Tests are marked `xfail` or `skip` or have comments about the bug until those bugs are fixed by devs.

---
## Visual Summary

```
run_tests.sh
  │
  ├── docker compose build test-runner     ← build your code & deps into container (using Playwright image)
  ├── docker compose run test-runner       ← run tests inside isolated env
  │     └─ pytest invokes Playwright, discovers, runs, reports, screenshots, traces
  └── docker compose down                  ← cleanup
```

---

## 8. CI Integration – Detailed Flow (GitHub Actions)

### **A. Triggering the Workflow**

* The workflow (see `.github/workflows/ci.yml`) is triggered automatically by:

  * A `push` to `master`
  * A scheduled CRON job (e.g., nightly)
  * A manual run via **workflow\_dispatch** (which allows for browser/environment selection). 
  **Unfortunately only authenticated users with write (push) access can actually start the workflow run**
  ![img.png](images/Readme/img.png)

---

### **B. Job Matrix & Browser Selection**

* The workflow uses a **matrix** to run tests for each:

  * Browser (`chromium`, `webkit`)
  * Test block/marker (`ui`, `api`, `usertests`, `cart`, `shopping_modal`, `product_details`)
* This means jobs run in parallel for combinations (e.g., UI+Chromium, UI+Webkit).

---

### **C. Steps in Each Job**

#### 1. **Checkout Repository**

* Uses `actions/checkout@v4` to get the latest source code.

#### 2. **Install Docker Compose**

* Ensures the CI environment (usually `ubuntu-latest`) has Docker Compose installed.

#### 3. **Environment File Preparation**

* Dynamically creates either `localconf_local.env` or `localconf_staging.env` based on workflow inputs:

  * **Security:** The contents of these files come from **GitHub Secrets**, not from the repository (keeps sensitive 
  data safe).

#### 4. **Show Test Context**

* Logs which testblock, environment, and browser are being run (handy for CI logs).

#### 5. **Run Tests via Bash Script**

* Executes `./run_tests.sh` with the right parameters:

  * `-b` for browser (chromium/webkit)
  * `-m` for test block
  * `-e` for environment (local/staging)
* All Docker orchestration and test logic runs exactly as described earlier.

#### 6. **Collect and Prepare Artifacts**

* After the test run, all generated artifacts (`report.html` and screenshots) are copied to a temporary output directory
  under the browser and test block. Examples: `out/chromium/ui/`, `out/webkit/ui/`, etc.

#### 7. **Publish Report to GitHub Pages**

* Uses [`peaceiris/actions-gh-pages`](https://github.com/peaceiris/actions-gh-pages) to publish the HTML report and screenshots to the `gh-pages` branch.
* **Result:** Test results are easily browsable at
  `https://<org>.github.io/<repo>/chromium/<block>/` or `/webkit/<block>/`.
   Working example: https://gwojacek.github.io/qa-demo-repository/chromium/usertests/


#### 8. **Log Report URLs**

* The workflow prints a clickable link to the report directly in the CI summary for convenience.

#### 9. **Summarize Environment in Workflow Summary**

* Adds a concise summary line (which block, browser, environment) to the **GitHub Actions summary** panel, improving 
auditability.

---

### **D. Key Security & Portability Points**

* **Secrets (env files)** are passed via [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets), never stored in your repo.
* **Docker and test logic is identical** in CI and locally.
* **Artifacts (reports, screenshots)** are published and preserved, making test results accessible even to 
non-developers.
