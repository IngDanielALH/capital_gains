# 📊 Capital Gains Calculator

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-green)
![Quality Gate](https://img.shields.io/badge/quality-A-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A robust **Command Line Interface (CLI)** application designed to calculate taxes on capital gains from stock market operations. It processes financial transaction records in compliance with configurable tax regulations, emphasizing **financial precision**, **scalability**, and **clean architecture**.

---

## 📋 Table of Contents
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Automation (Makefile)](#-automation-makefile)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Running with Docker](#-running-with-docker)
- [Testing & Quality](#-testing--quality)
- [Technical Decisions](#-technical-decisions)

---

## 🚀 Features

### Business Logic
- **Weighted Average Price (WAP)**: Automatically recalculates asset valuation upon every purchase.
- **Tax Rules Engine**: Applies tax rates only when profits exceed the configured threshold (e.g., $20,000).
- **Loss Deduction**: Automatically carries forward losses to offset future taxable gains.

### Technical Highlights
- **SOLID Principles**: Implements the **Strategy Pattern** to handle operations (Buy/Sell), adhering to the Open/Closed Principle (OCP).
- **High Precision Arithmetic**: Utilizes Python's `decimal.Decimal` with `ROUND_HALF_UP` strategy to eliminate floating-point calculation errors.
- **Memory Efficiency (Streaming)**: Implements **Lazy Loading** via Python Generators (`yield`). The application processes input line-by-line, allowing it to handle massive datasets with constant memory usage (O(1)).
- **Optimized Data Structures**: Uses `__slots__` in DTOs to reduce memory overhead by approximately 40% per object.

---

## 📂 Project Structure

The project follows standard Python naming conventions (`snake_case` for modules, `PascalCase` for classes).

```text
capital_gains/
├── capital_gains/          # Source Code Package
│   ├── __main__.py         # Application Entry Point
│   ├── configuration/      # Configuration Logic
│   │   └── config_loader.py
│   ├── dto/                # Data Transfer Objects (Memory Optimized)
│   │   ├── tax_dto.py
│   │   └── transaction_dto.py
│   ├── service/            # Core Business Logic
│   │   ├── gains_service.py
│   │   └── portfolio_state.py
│   └── utils/              # Shared Utilities
│       ├── constants.py
│       └── math_utils.py
├── tests/                  # Test Suite
│   ├── integration/        # End-to-end scenarios
│   ├── unit/               # Isolated unit tests
│   └── resources/          # Test data samples
├── config.yml              # Externalized configuration rules
├── Dockerfile              # Container definition
├── Makefile                # Automation scripts
├── requirements.txt        # Dependencies
└── sonar-project.properties # Static Analysis Config
   ```

## 🛠️ Installation & Setup
- This project requires Python 3.9+.

Install dependencies:
 ```bash
   pip install -r requirements.txt
   ```
Or simply
```bash
   make install
   ```

## ⚡ Automation (Makefile)

To simplify common development tasks, a `Makefile` is included. You can use the following commands instead of typing long instructions:

| Command                       | Description                                      |
|:------------------------------|:-------------------------------------------------|
| `make install`                | Installs project dependencies (`requirements.txt`). |
| `make test`                   | Runs the full test suite with verbose output.    |
| `make run`                    | Runs the application in interactive mode.        |
| `make docker-build`           | Builds the Docker image.                         |
| `make docker-run`             | Runs the application inside a Docker container.  |
| `make clean`                  | Removes cache files, build artifacts, and logs.  |
| `make sonar token=...`        | Runs SonarQube analysis (requires local server).  |

## 📌 Configuration

The application rules are decoupled from the source code using config.yml. This allows for easy adjustments to tax laws without redeploying code.

Default config.yml:
```yaml
app:
  name: "Capital Gains"
  version: "1.0"

taxes:
  sell:
    percentage: 20.0
    limit_without_taxes: 20000
   ```

## 📝 Usage

The application reads a stream of JSON arrays from Standard Input (stdin) and prints the results to Standard Output (stdout).
Input Format

Each line must contain a valid JSON array representing a sequence of operations.

Example Input:
```json
[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}, {"operation":"sell", "unit-cost":20.00, "quantity": 5000}]
[{"operation":"buy", "unit-cost":20.00, "quantity": 10000}, {"operation":"sell", "unit-cost":10.00, "quantity": 5000}]
```  
Execution

Option 1: Using File Redirection (Recommended) Prepare an input.txt file and pipe it into the application:
```bash
   python -m capital_gains.main < input.txt
   ```
Option 2: Interactive Mode Run the command and paste JSON lines into the terminal:
```bash
   python -m capital_gains.main
   ```
Or use
```bash
   make run
   ```
Expected Output
```json
[{"tax": 0.00}, {"tax": 10000.00}]
[{"tax": 0.00}, {"tax": 0.00}]
```

### 🐳 Running with Docker

Build the image:
```bash
docker build -t capital-gains .
   ```
Or use
```bash
make docker-build
   ```
Run with input file:
```bash
docker run -i --rm capital-gains < input.txt
   ```
  
## 🧪 Testing
The project maintains high standards of code quality and test coverage.

Run all tests:
```bash
   python -m pytest tests/ -v
   ```
Or use
```bash
   make test
   ```

Sample Output:
```
================ test session starts =================
platform darwin -- Python 3.9.6, pytest-8.3.5
rootdir: /.../capital_gains
collected 12 items

tests/integration_tests/test_gain_service.py ......... [ 75%]
tests/integration_tests/test_main_function.py ..       [ 91%]
tests/unit_tests/test_round.py .                       [100%]

================ 12 passed in 0.14s ==================
```  
Static Analysis (SonarQube)

A sonar-project.properties file is included to facilitate static analysis. The project enforces strict quality gates regarding:

    Code Coverage: > 90%

    Cognitive Complexity: Low complexity per function.

    Maintainability: 'A' rating.

To run the analysis locally (requires Docker):
```bash
   make sonar token=<your-sonar-token>
   ```

## 🧠 Technical Decisions
### 1. Lazy Loading & Generators
Instead of loading the entire input file into a list (which could crash memory with large files), the application processes data as a stream.

- **Why?** Scalability. It allows processing gigabytes of transaction logs with minimal RAM.
- **Implementation:** The `main` function iterates `sys.stdin` line-by-line, and the `GainsService` yields results one by one using Python generators.

### 2. Decimal Precision
Financial applications cannot rely on standard floating-point math (e.g., `0.1 + 0.2 != 0.3`).

- **Solution:** All monetary calculations use `decimal.Decimal`.
- **Rounding:** Strict `ROUND_HALF_UP` rounding is applied at specific calculation steps as per business requirements.

### 3. Memory Slots
The `TransactionDTO` class uses `__slots__`.

- **Why?** Standard Python objects use a dynamic `__dict__` to store attributes. Using `__slots__` tells Python to reserve fixed memory space, reducing the memory footprint of millions of transaction objects by ~40-50%.
### 4. Strategy Pattern (OCP)

The logic for buy and sell operations is encapsulated in separate Strategy classes inheriting from OperationStrategy.

- Why? To adhere to the Open/Closed Principle. New operations (e.g., "split", "dividend") can be added by creating a new class without modifying the core processing loop.