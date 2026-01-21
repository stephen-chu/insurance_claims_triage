"""Check the status of a run."""

import sys
from langgraph_sdk import get_sync_client

DEPLOYMENT_URL = "https://insurance-claims-agent-1d71606fdb2e59c4b10c2d85d0ca197c.us.langgraph.app"


def check_run(thread_id: str):
    """Check run status and state."""
    client = get_sync_client(url=DEPLOYMENT_URL)

    # Get thread state
    state = client.threads.get_state(thread_id)
    print(f"Thread: {thread_id}")
    print(f"Status: {state.get('status', 'unknown')}")
    print(f"Next: {state.get('next', [])}")

    if state.get('values'):
        messages = state['values'].get('messages', [])
        print(f"\nMessages ({len(messages)}):")
        for msg in messages[-5:]:  # Last 5 messages
            role = msg.get('type', msg.get('role', 'unknown'))
            content = msg.get('content', '')[:200]
            print(f"  [{role}]: {content}...")

    if state.get('tasks'):
        print(f"\nPending tasks (interrupts):")
        for task in state['tasks']:
            print(f"  {task}")


def list_threads():
    """List recent threads."""
    client = get_sync_client(url=DEPLOYMENT_URL)
    threads = client.threads.list(limit=10)
    print("Recent threads:")
    for t in threads:
        print(f"  {t['thread_id']} - {t.get('created_at', '')}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_run.py <thread_id>")
        print("       python check_run.py --list")
        sys.exit(1)

    if sys.argv[1] == "--list":
        list_threads()
    else:
        check_run(sys.argv[1])
