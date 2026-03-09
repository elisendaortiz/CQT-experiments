#!/bin/bash
set -euo pipefail

# dev_env = any virtual env you'd like to use for specific development needs
ENV_DIR=~/envs/dev_env

# Load qibo module, unset python path, Create fresh dev_env
module load qibo
unset PYTHONPATH
python3 -m venv "$ENV_DIR"
source "$ENV_DIR/bin/activate"
pip install --upgrade pip

# Install whichever editable local packages you want to use in dev_env
pip install -e ~/qibocal-eo-fork
pip install -e ~/CQT-experiments-eo-fork

# Add module site-packages as fallback (for keysight + its deps).
# Named zzz_* so it sorts AFTER any editable install .pth files
# (e.g. qibocal.pth, qibolab.pth), ensuring dev_env always wins.
VENV_SITE=$(python3 -c 'import site; print(site.getsitepackages()[0])')
MODULE_SITE="/mnt/scratch/envs/qibo/lib/python3.12/site-packages"

echo "$MODULE_SITE" > "$VENV_SITE/zzz_module_fallback.pth"
echo "Created $VENV_SITE/zzz_module_fallback.pth → $MODULE_SITE"

# 4. Log all installed versions for clarity
echo ""
echo "===== INSTALLED PACKAGES ====="
pip list | grep -iE "qibo|qibocal|qibolab|qiboml|qibo-client"
echo ""
echo "===== qibocal location ====="
pip show qibocal | grep -E "^(Name|Version|Location|Editable)"
echo "=============================="
