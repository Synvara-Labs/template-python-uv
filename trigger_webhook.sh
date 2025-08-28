#!/bin/bash

# Webhook trigger script for PR #8
# This script sends a properly formatted GitHub pull_request webhook event

curl -X POST https://synvara.app.n8n.cloud/webhook-test/github-pr-webhook \
    -H "Content-Type: application/json" \
    -H "X-GitHub-Event: pull_request" \
    -H "X-GitHub-Delivery: test-$(date +%s)" \
    -d '{
      "action": "synchronize",
      "number": 8,
      "pull_request": {
        "id": "PR_kwDOPkIoqc6lnd-B",
        "number": 8,
        "state": "open",
        "locked": false,
        "title": "feat: Improve example module with validation and comprehensive tests",
        "body": "This PR addresses all code review feedback by implementing input validation, comprehensive tests, and improved documentation. It includes 52+ parameterized tests, security improvements, and production-ready error handling.",
        "url": "https://api.github.com/repos/Synvara-Labs/template-python-uv/pulls/8",
        "html_url": "https://github.com/Synvara-Labs/template-python-uv/pull/8",
        "diff_url": "https://github.com/Synvara-Labs/template-python-uv/pull/8.diff",
        "patch_url": "https://github.com/Synvara-Labs/template-python-uv/pull/8.patch",
        "user": {
          "login": "lance0821",
          "id": 4596483,
          "type": "User"
        },
        "head": {
          "ref": "feat/example-module-improvements",
          "sha": "98500ee",
          "repo": {
            "name": "template-python-uv",
            "full_name": "Synvara-Labs/template-python-uv",
            "owner": {
              "login": "Synvara-Labs",
              "type": "Organization"
            }
          }
        },
        "base": {
          "ref": "main",
          "sha": "3b644d5",
          "repo": {
            "name": "template-python-uv",
            "full_name": "Synvara-Labs/template-python-uv",
            "owner": {
              "login": "Synvara-Labs",
              "type": "Organization"
            }
          }
        },
        "merged": false,
        "mergeable": true,
        "mergeable_state": "clean",
        "commits": 9,
        "additions": 739,
        "deletions": 138,
        "changed_files": 8
      },
      "repository": {
        "name": "template-python-uv",
        "full_name": "Synvara-Labs/template-python-uv",
        "owner": {
          "login": "Synvara-Labs",
          "type": "Organization"
        },
        "html_url": "https://github.com/Synvara-Labs/template-python-uv",
        "description": "Python project template with uv package manager",
        "private": true,
        "default_branch": "main"
      },
      "sender": {
        "login": "lance0821",
        "id": 4596483,
        "type": "User"
      }
    }'