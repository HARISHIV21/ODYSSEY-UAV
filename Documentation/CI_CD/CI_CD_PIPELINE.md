# ODYSSEY — Continuous Integration and Delivery

## Overview

ODYSSEY uses GitHub Actions to automate software validation and
versioned source-code releases.

## Continuous Integration

Workflow: `.github/workflows/ci.yml`

Triggers:
- Push to main
- Push to feature branches
- Pull requests targeting main
- Manual workflow dispatch

Pipeline:
1. Checkout repository.
2. Configure Python 3.12.
3. Install project dependencies.
4. Compile Python modules.
5. Execute automated pytest tests.
6. Upload JUnit XML and test logs.

The CI workflow validates the automated software test suite.
It does not launch PX4 SITL or Gazebo.

## Continuous Delivery

Workflow: `.github/workflows/release.yml`

Trigger:
- Push a version tag matching v*

Pipeline:
1. Checkout the tagged source revision.
2. Install dependencies.
3. Compile Python modules.
4. Execute automated tests.
5. Package the tagged source as ZIP and TAR.GZ.
6. Generate SHA-256 checksums.
7. Publish a GitHub Release with the generated assets.

This is a versioned source-code delivery process.
It does not deploy to a physical UAV.

## Local validation

Run:

    python -m compileall -q MissionComputer Navigation Control Core Communication Sensors Telemetry Utils

    python -m pytest -v

## Release example

After the validated changes have been committed and pushed:

    git tag -a v1.0.0 -m "ODYSSEY validated release"
    git push origin v1.0.0

The release workflow then validates and publishes that tagged revision.

## Current validation scope

Automated tests cover mission validation, connection handling,
navigation, telemetry stream failures, landing confirmation,
disarming confirmation and failsafe behaviour.

Physical UAV testing and hardware-in-the-loop validation are
outside the scope of these workflows.
