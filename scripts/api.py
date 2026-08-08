#!/usr/bin/env python3
"""GoalsWon REST API helper for operations not available in the CLI."""

import argparse
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path


def load_api_key() -> str:
    config_path = Path.home() / ".goalswon" / "config.json"
    try:
        with open(config_path) as f:
            return json.load(f)["apiKey"]
    except (FileNotFoundError, KeyError):
        print(json.dumps({"error": f"Could not read API key from {config_path}"}))
        sys.exit(1)


def request(method: str, path: str, body: dict | None = None) -> dict:
    api_key = load_api_key()
    url = f"https://api.goalswon.com/api/v1{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "X-GoalsWon-Key": api_key,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def cmd_chat_send(args):
    # Enforce AI authorship attribution at the tool level so it can never be
    # forgotten by the caller. If the message already carries an attribution
    # prefix, leave it untouched.
    text = args.text
    stripped = text.lstrip()
    if not (stripped.startswith("[AI message]") or stripped.startswith("[Automated message]")):
        text = f"[AI message] {text}"
    result = request("POST", "/chat/messages", {"text": text})
    print(json.dumps(result, indent=2))


def cmd_targets_delete(args):
    result = request("DELETE", f"/targets/{args.id}")
    print(json.dumps(result, indent=2))


def cmd_targets_update(args):
    body = {}
    if args.name:
        body["name"] = args.name
    if args.yearly_target_id is not None:
        body["yearlyTargetId"] = args.yearly_target_id if args.yearly_target_id != "null" else None
    if args.tag:
        body["tag"] = args.tag
    if args.description is not None:
        body["description"] = args.description
    if not body:
        print(json.dumps({"error": "No fields to update provided"}))
        sys.exit(1)
    result = request("PUT", f"/targets/{args.id}", body)
    print(json.dumps(result, indent=2))


def cmd_targets_get(args):
    result = request("GET", f"/targets/{args.id}")
    print(json.dumps(result, indent=2))


def cmd_yearly_targets_list(args):
    result = request("GET", "/yearly-targets")
    print(json.dumps(result, indent=2))


def cmd_yearly_targets_get(args):
    result = request("GET", f"/yearly-targets/{args.id}")
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description="GoalsWon API helper")
    sub = parser.add_subparsers(dest="command", required=True)

    # chat send
    p_chat = sub.add_parser("chat-send", help="Send a message to your coach")
    p_chat.add_argument("text", help="Message text")
    p_chat.set_defaults(func=cmd_chat_send)

    # targets delete
    p_tdel = sub.add_parser("targets-delete", help="Delete a monthly target")
    p_tdel.add_argument("id", help="Target ID")
    p_tdel.set_defaults(func=cmd_targets_delete)

    # targets update
    p_tupd = sub.add_parser("targets-update", help="Update a monthly target")
    p_tupd.add_argument("id", help="Target ID")
    p_tupd.add_argument("--name", help="New name")
    p_tupd.add_argument("--yearly-target-id", help='Yearly target ID to link (or "null" to unlink)')
    p_tupd.add_argument("--tag", help="Colour tag")
    p_tupd.add_argument("--description", help="Description text")
    p_tupd.set_defaults(func=cmd_targets_update)

    # targets get
    p_tget = sub.add_parser("targets-get", help="Get a single monthly target")
    p_tget.add_argument("id", help="Target ID")
    p_tget.set_defaults(func=cmd_targets_get)

    # yearly-targets list
    p_ytl = sub.add_parser("yearly-targets-list", help="List yearly targets")
    p_ytl.set_defaults(func=cmd_yearly_targets_list)

    # yearly-targets get
    p_ytg = sub.add_parser("yearly-targets-get", help="Get a yearly target with linked monthly targets")
    p_ytg.add_argument("id", help="Yearly target ID")
    p_ytg.set_defaults(func=cmd_yearly_targets_get)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
