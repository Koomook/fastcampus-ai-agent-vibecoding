"""CLI entry point for Playwright MCP Client."""

import argparse
import asyncio
import sys

from .agent import ClaudeAgent
from .client import PlaywrightMCPClient
from .config import Config


async def run_single_command(user_input: str) -> None:
    """Run a single command and exit.

    Args:
        user_input: User's command to execute.
    """
    try:
        # Load configuration
        config = Config.from_env()
        config.ensure_output_dir()

        # Connect to MCP server
        async with PlaywrightMCPClient(config) as mcp_client:
            # Initialize agent
            agent = ClaudeAgent(config, mcp_client)
            await agent.initialize()

            print(f"\n> {user_input}")
            print()

            # Process request
            response = await agent.process_request(user_input)
            print(response)
            print()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


async def run_interactive() -> None:
    """Run in interactive mode."""
    try:
        # Load configuration
        config = Config.from_env()
        config.ensure_output_dir()

        print("Playwright MCP Client - Interactive Mode")
        print("Type 'exit' or 'quit' to exit")
        print()

        # Connect to MCP server
        async with PlaywrightMCPClient(config) as mcp_client:
            # Initialize agent
            agent = ClaudeAgent(config, mcp_client)
            await agent.initialize()

            print(f"Connected to Playwright MCP Server")
            print(f"Available tools: {len(agent.tools)}")
            print()

            # Interactive loop
            while True:
                try:
                    user_input = input("> ").strip()

                    if not user_input:
                        continue

                    if user_input.lower() in ["exit", "quit"]:
                        print("Goodbye!")
                        break

                    # Process request
                    response = await agent.process_request(user_input)
                    print()
                    print(response)
                    print()

                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    break
                except EOFError:
                    print("\nGoodbye!")
                    break

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Playwright MCP Client - AI-powered browser automation"
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to execute (if not provided, runs in interactive mode)",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode",
    )

    args = parser.parse_args()

    # Determine mode
    if args.interactive or args.command is None:
        # Interactive mode
        asyncio.run(run_interactive())
    else:
        # Single command mode
        asyncio.run(run_single_command(args.command))


if __name__ == "__main__":
    main()
