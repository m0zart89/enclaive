#!/usr/bin/env bash
cd "$(dirname "$0")"
SHA="$(git rev-parse --short HEAD)"
docker build -t "app:${SHA}" -t app:latest .
