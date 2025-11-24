#!/usr/bin/env bash
set -euo pipefail

SCRIPTS_DIR="/app/scripts"

# Mode: "migrate-only" runs only the two migration scripts.
# Any other mode (default) runs all four scripts in the order below.
MODE="${1:-}"

cd /app

run_script() {
  local f="$1"
  if [ -f "${SCRIPTS_DIR}/${f}" ]; then
    echo "Running ${f}"
    # prefer module form if package, fall back to file
    python -m "scripts.${f%.*}" 2>/dev/null || python "${SCRIPTS_DIR}/${f}"
  else
    echo "Skipping ${f} (not found)"
  fi
}



if [ "${MODE}" = "migrate-only" ]; then
  # Run only the migration scripts, then exit
  run_script "master_tbl_migration.py"
  run_script "store_migration.py"
  run_script "ledger_migration.py"
  run_script "jobmaster_migration.py"
  run_script "cds_migration.py"
  echo "Migrations complete (migrate-only). Exiting."
  exit 0
fi

# Default: run all steps (file creation then migrations)
run_script "File_creation_1.py"
run_script "File_creation_2.py"
run_script "master_tbl_migration.py"
run_script "store_migration.py"
run_script "ledger_migration.py"
run_script "File_creation_3.py"
run_script "File_creation_4.py"
run_script "jobmaster_migration.py"
run_script "File_creation_5.py"
run_script "cds_migration.py"

# Hand off to CMD (exec to replace shell with the process)
exec "$@"
