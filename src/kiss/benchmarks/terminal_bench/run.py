# Author: Koushik Sen (ksen@berkeley.edu)

"""Run Terminal-Bench 2.0 with the sorcar harbor agent.

Usage:
    python -m kiss.benchmarks.terminal_bench.run \
        --model anthropic/claude-opus-4-6 \
        --n-concurrent 8

This uses harbor's --agent-import-path flag to load our custom
SorcarHarborAgent without needing to modify the harbor source.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

AGENT_IMPORT_PATH = "kiss.benchmarks.terminal_bench.agent:SorcarHarborAgent"


def run_terminal_bench(
    model: str = "anthropic/claude-opus-4-6",
    dataset: str = "terminal-bench@2.0",
    n_concurrent: int = 8,
    trials: int = 1,
) -> None:
    """Run Terminal-Bench 2.0 using the harbor CLI with the sorcar agent.

    Args:
        model: Model name in harbor format (provider/model).
        dataset: Harbor dataset specifier (e.g. "terminal-bench@2.0").
        n_concurrent: Number of concurrent task containers.
        trials: Number of attempts per task (-k flag). Use 5 for leaderboard.
    """
    cmd = [
        "harbor",
        "run",
        "--dataset",
        dataset,
        "--agent-import-path",
        AGENT_IMPORT_PATH,
        "--model",
        model,
        "--n-concurrent",
        str(n_concurrent),
        "-k",
        str(trials),
    ]

    print(f"Running: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print(
            "ERROR: 'harbor' CLI not found. Install with: uv pip install harbor",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: harbor exited with code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)


def main() -> None:
    """CLI entry point for Terminal-Bench 2.0 runner."""
    parser = argparse.ArgumentParser(
        description="Run Terminal-Bench 2.0 with sorcar agent"
    )
    parser.add_argument(
        "--model",
        default="anthropic/claude-opus-4-6",
        help="Model name in provider/model format",
    )
    parser.add_argument(
        "--dataset",
        default="terminal-bench@2.0",
        help="Harbor dataset specifier",
    )
    parser.add_argument(
        "--n-concurrent",
        type=int,
        default=8,
        help="Number of concurrent containers",
    )
    parser.add_argument(
        "-k",
        "--trials",
        type=int,
        default=1,
        help="Number of attempts per task (use 5 for leaderboard submission)",
    )
    args = parser.parse_args()
    run_terminal_bench(args.model, args.dataset, args.n_concurrent, args.trials)


if __name__ == "__main__":
    main()
