#!/bin/bash

# Extract and save YouTube transcript from PostToolUse hook input
# Input: JSON via stdin with tool_response array format
# Output: Saves transcript to logs/{sanitized_title}.txt

set -euo pipefail

readonly OUTPUT_DIR="logs"

sanitize_filename() {
    local filename="$1"
    # Remove " - YouTube" suffix
    filename="${filename% - YouTube}"
    # Replace spaces and special chars with underscores
    filename=$(echo "$filename" | sed 's/[^a-zA-Z0-9]/_/g')
    # Remove consecutive underscores
    filename=$(echo "$filename" | sed 's/__*/_/g')
    # Remove leading/trailing underscores
    filename=$(echo "$filename" | sed 's/^_//;s/_$//')
    # Lowercase and limit length
    filename=$(echo "$filename" | tr '[:upper:]' '[:lower:]' | cut -c1-100)
    echo "$filename"
}

main() {
    local json_input response_data title transcript sanitized_title output_file

    # Read stdin
    json_input=$(cat)

    # Extract response data
    response_data=$(echo "$json_input" | jq -r '.tool_response[0].text // empty')

    # Parse title and transcript
    title=$(echo "$response_data" | jq -r '.title // empty')
    transcript=$(echo "$response_data" | jq -r '.transcript // empty')

    # Save if transcript exists
    if [[ -n "$transcript" ]]; then
        # Generate filename from title or use default
        if [[ -n "$title" ]]; then
            sanitized_title=$(sanitize_filename "$title")
            output_file="${OUTPUT_DIR}/${sanitized_title}.txt"
        else
            output_file="${OUTPUT_DIR}/youtube-transcript.txt"
        fi

        mkdir -p "$OUTPUT_DIR"
        echo "$transcript" > "$output_file"
    fi
}

main
