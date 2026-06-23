#!/bin/bash
# Jira API helper — source this file or use as CLI
# Usage: source .claude/scripts/jira.sh
#   jira me           — current user
#   jira projects     — list projects
#   jira search JQL   — search issues
#   jira get KEY      — get issue
#   jira browse KEY   — open issue in browser

JIRA_CONF="$HOME/ClaudeProjects/ai-mission/.claude/jira-config.json"

if [ ! -f "$JIRA_CONF" ]; then
  echo "❌ Config not found: $JIRA_CONF" >&2
  return 1 2>/dev/null || exit 1
fi

JIRA_URL=$(python3 -c "import json; print(json.load(open('$JIRA_CONF'))['url'])")
JIRA_TOKEN=$(python3 -c "import json; print(json.load(open('$JIRA_CONF'))['token'])")

jira() {
  local cmd="${1:-help}"
  shift 2>/dev/null || true

  case "$cmd" in
    me|whoami|self)
      curl -s -H "Authorization: Bearer $JIRA_TOKEN" "$JIRA_URL/rest/api/2/myself" | python3 -m json.tool
      ;;
    projects|project)
      curl -s -H "Authorization: Bearer $JIRA_TOKEN" "$JIRA_URL/rest/api/2/project" | python3 -m json.tool
      ;;
    search|jql|find)
      local jql="$*"
      [ -z "$jql" ] && jql="assignee=currentUser()"
      local encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$jql'))")
      curl -s -H "Authorization: Bearer $JIRA_TOKEN" "$JIRA_URL/rest/api/2/search?jql=$encoded&maxResults=20" | python3 -m json.tool
      ;;
    get|issue|view)
      [ -z "$1" ] && { echo "Usage: jira get PROJECT-123" >&2; return 1; }
      curl -s -H "Authorization: Bearer $JIRA_TOKEN" "$JIRA_URL/rest/api/2/issue/$1" | python3 -m json.tool
      ;;
    browse|open)
      [ -z "$1" ] && { echo "Usage: jira browse PROJECT-123" >&2; return 1; }
      open "$JIRA_URL/browse/$1"
      ;;
    api)
      # Raw API call — jira api /rest/api/2/search?jql=...
      local path="$1"
      shift
      curl -s -H "Authorization: Bearer $JIRA_TOKEN" "$JIRA_URL$path" "$@"
      ;;
    help|--help|-h)
      echo "Jira CLI helpers:"
      echo "  jira me          — current user info"
      echo "  jira projects    — list projects"
      echo "  jira search JQL  — search (default: my issues)"
      echo "  jira get KEY     — show issue details"
      echo "  jira browse KEY  — open in browser"
      echo "  jira api PATH    — raw REST call"
      ;;
    *)
      echo "Unknown: $cmd (try: jira help)" >&2
      return 1
      ;;
  esac
}

echo "✅ Jira helper loaded — use: jira help"
