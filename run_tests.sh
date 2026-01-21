#!/usr/bin/env bash

set -euo pipefail

export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)

BROWSER="chromium" # chromium | webkit
MARKER=""
WORKERS="auto"
HEADED=false
DEBUG=false
TRACING=false
ENV_TYPE="local"
RERUNS=1

usage(){
cat <<EOF >&2
Usage: $0 [-b chromium|webkit] [-m <marker>] [-n <workers>] [-H] [-D] [-T] [-e <env_type>] [-r <reruns>]
-b browser (chromium|webkit), default=chromium
-m pytest marker
-n xdist workers, default=auto
-H run in headed mode
-D enable Playwright Inspector (PWDEBUG=1)
-T enable Playwright tracing (--tracing=retain-on-failure) for trace viewer debugging on failed tests
-e environment type (local|staging), default=local
-r number of reruns for failed tests, default=1
EOF
exit 1;
}

while getopts "b:m:n:He:r:DT" opt; do
  case $opt in
    b) BROWSER="$OPTARG" ;;
    m) MARKER="$OPTARG" ;;
    n) WORKERS="$OPTARG" ;;
    H) HEADED=true ;;
    D) DEBUG=true ;;
    T) TRACING=true ;;
    e) ENV_TYPE="$OPTARG" ;;
    r) RERUNS="$OPTARG" ;;
    *) usage ;;
  esac
done

# ---------------------------
# Inspector behavior
# ---------------------------
if [ "$DEBUG" = true ]; then
  echo "🐞 Inspector enabled → forcing headed mode + xdist workers = 1"
  HEADED=true
  WORKERS=1
fi


# ---------------------------
# Tracing checks
# ---------------------------
if [ "$TRACING" = true ]; then
  echo "🔍 Tracing enabled (retain on failure) → traces will be saved only for failed tests in tests/artifacts"
fi

# ---------------------------
# X11 forwarding for headed mode
# ---------------------------
EXTRA_DOCKER_ARGS=""
if [ "$HEADED" = true ]; then
  EXTRA_DOCKER_ARGS="-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY"
fi

# Always mount artifacts volume to persist traces and reports
EXTRA_DOCKER_ARGS="$EXTRA_DOCKER_ARGS -v $PWD/tests/artifacts:/app/tests/artifacts"

echo "🧹 Shutting down any old containers…"
docker compose down --remove-orphans

echo "🧹 Cleaning artifacts…"
rm -rf tests/artifacts && mkdir -p tests/artifacts

echo "📦 Building test-runner…"
docker compose build test-runner

PYTEST_ARGS=(-v --color=yes)
[ -n "$MARKER" ] && PYTEST_ARGS+=( -m "$MARKER" )
[ "$HEADED" = true ] && PYTEST_ARGS+=( --headed )
[ "$TRACING" = true ] && PYTEST_ARGS+=( --tracing=retain-on-failure --output=tests/artifacts )
PYTEST_ARGS+=( --browser "$BROWSER" )
PYTEST_ARGS+=( -n "$WORKERS" --reruns "$RERUNS" )
PYTEST_ARGS+=( --html=tests/artifacts/report.html --self-contained-html )

echo "🧪 Running pytest ($BROWSER, headed=false, workers=$WORKERS, debug=$DEBUG, tracing=$TRACING, env=$ENV_TYPE)…"

# Run Docker directly - you'll see output in real-time
# Use || true to prevent script from exiting on test failures
docker compose run --rm --no-deps \
  $EXTRA_DOCKER_ARGS \
  -e ENV_TYPE="$ENV_TYPE" \
  -e PWDEBUG=$([ "$DEBUG" = true ] && echo 1 || echo 0) \
  --entrypoint pytest \
  test-runner \
  "${PYTEST_ARGS[@]}" || EXITCODE=$?

# If EXITCODE wasn't set by failure, it means tests passed
EXITCODE=${EXITCODE:-0}

# IMPORTANT: Check for traces BEFORE tearing down docker
if [ "$TRACING" = true ]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔍 TRACE VIEWER COMMANDS FOR FAILED TESTS"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  TRACE_FILES=$(find tests/artifacts -type f -name "*.zip" 2>/dev/null | sort)

  if [ -n "$TRACE_FILES" ]; then
    TRACE_COUNT=0
    while IFS= read -r trace; do
      TRACE_COUNT=$((TRACE_COUNT + 1))
      TEST_NAME=$(basename "$trace" .zip)
      echo ""
      echo "📊 Test #$TRACE_COUNT: $TEST_NAME"
      echo "npx playwright show-trace $(realpath "$trace")"
    done <<< "$TRACE_FILES"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ Found $TRACE_COUNT trace file(s) - Copy any command above to view the trace"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  else
    echo "✅ No trace files found - All tests passed!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  fi
  echo ""
fi

echo "🧹 Tearing down…"
docker compose down

echo ""
echo "🏁 Report: file://$(realpath tests/artifacts/report.html)"

exit $EXITCODE