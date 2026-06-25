#!/bin/bash

while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" =~ ^# ]] && continue

    encoded=$(printf "%s" "$value" | base64 -w 0)
    printf "SECRET_%s=%s\n" "$key" "$encoded"
done < .env > .env_encoded