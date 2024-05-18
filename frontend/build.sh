#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Ensure that SRC_PKG and DEPLOY_PKG variables are set
if [ -z "$SRC_PKG" ]; then
  echo "SRC_PKG is not set. Please set it to the source package directory."
  exit 1
fi

if [ -z "$DEPLOY_PKG" ]; then
  echo "DEPLOY_PKG is not set. Please set it to the deployment package directory."
  exit 1
fi

# Install the required packages into the source package directory
pip3 install -r "${SRC_PKG}/requirements.txt" -t "${SRC_PKG}"

# Copy the source package directory to the deployment package directory
cp -r "${SRC_PKG}" "${DEPLOY_PKG}"

echo "Packages installed and copied to deployment directory successfully."