# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Capital Gains Calculator - a Python CLI that computes taxes on stock market operations. Reads JSON arrays from stdin, outputs tax results to stdout. Uses `decimal.Decimal` with `ROUND_HALF_UP` for financial precision.

## Commands

```bash
make setup          # Create .venv and install dependencies
make test           # Run full test suite (pytest)
make run            # Run app interactively (reads from stdin)
make clean          # Remove caches, coverage, .venv

# Run a single test
.venv/bin/python -m pytest tests/integration/test_gain_service.py::test_case_1 -v

# Run with file input
.venv/bin/python -m capital_gains < input.txt

# Docker
make docker         # Build and run in one step
```

## Architecture

**Entry point:** `capital_gains/__main__.py` - reads stdin line-by-line, delegates to `GainsService`.

**Strategy Pattern** for operations:
- `OperationStrategy` (ABC) in `service/portfolio_state.py`
- `BuyStrategy` - recalculates Weighted Average Price (WAP), no tax event
- `SellStrategy` - handles profit/loss calculation, tax application, loss deduction
- Strategies registered in `STRATEGIES` dict keyed by operation type constants

**`PortfolioState`** (mutable context) tracks: `weighted_average_price`, `total_quantity`, `total_lose`, consecutive validation errors, and account blocking (blocks after 3 consecutive errors).

**`GainsService.parse_operations()`** is a generator that yields results one at a time for O(1) memory usage.

**Tax rules** (from `config.yml`): 20% tax rate, $20,000 exemption threshold. Losses carry forward and offset future gains.

**DTOs** use `__slots__` for memory optimization. `TransactionDTO` has a Builder pattern.

## Key Conventions

- All monetary math uses `decimal.Decimal`, never `float` for intermediate calculations
- `ROUND_HALF_UP` rounding applied at specific calculation steps via `Decimal.quantize()`
- Weighted Average Price recalculated on every buy (see `utils/math_utils.py`)
- Python `snake_case` for modules, `PascalCase` for classes
- Language: codebase comments and docstrings mix Spanish and English
- Tests organized as `tests/integration/` and `tests/unit/`
