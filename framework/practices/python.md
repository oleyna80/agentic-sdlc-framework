# Python Best Practices

> Coding standards for Python in Agentic SDLC projects.

---

## Code Style

```python
# Good — Type hints, concise
def calc_delta(spot: float, strike: float, iv: float) -> float:
    """Calculate option delta using Black-Scholes."""
    return bs_delta(spot, strike, iv)

# Avoid — No types, verbose docstring
def calculate_delta(spot_price, strike_price, implied_volatility):
    """
    Calculate the delta of an option using the Black-Scholes model.
    ...
    """
    return black_scholes_delta(spot_price, strike_price, implied_volatility)
```

## Key Rules

- **Type hints:** Always for function signatures
- **Docstrings:** One-line for simple functions, detailed for complex
- **Variable names:** Short when clear (`i`, `j`, `df`, `val`), descriptive when not
- **Error handling:** Use try/except, log errors
- **Async:** Use when doing I/O (API calls, DB queries)
- **Testing:** Write tests for critical paths

## Project Structure

```
project/
├── venv/              # Virtual environment
├── src/               # Source code
│   ├── api/          # API endpoints
│   ├── core/         # Business logic
│   └── utils/        # Helpers
├── tests/            # Tests
├── .env.example      # Example environment vars
└── requirements.txt  # Dependencies
```
