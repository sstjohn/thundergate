#!/bin/sh
# Regenerate public/og.png from the /og route.
#
# Builds the site, serves dist/ on a local port, screenshots
# http://127.0.0.1:$PORT/og/ with headless Chrome at 2x DPR,
# downsizes to the canonical 1200x630, and tears the server down.
#
# Run from the site repo root: scripts/make-og.sh

set -eu

PORT=8765
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

cd "$ROOT"
npm run build

python3 -m http.server "$PORT" --directory dist >/tmp/og-server.log 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT INT TERM

# Wait for the server to accept connections.
for _ in 1 2 3 4 5; do
    if curl -fs "http://127.0.0.1:$PORT/og/" >/dev/null 2>&1; then
        break
    fi
    sleep 0.3
done

"$CHROME" \
    --headless=new \
    --disable-gpu \
    --hide-scrollbars \
    --force-device-scale-factor=2 \
    --window-size=1200,630 \
    --screenshot="$ROOT/public/og.png" \
    "http://127.0.0.1:$PORT/og/"

sips -z 630 1200 "$ROOT/public/og.png" >/dev/null
file "$ROOT/public/og.png"
echo "wrote $ROOT/public/og.png"
