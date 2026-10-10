# Python Fundamentals for Practical Projects

## 1. Why Python is used
Python is a general-purpose programming language known for readable syntax and a broad ecosystem. It is used in automation, web services, data analysis, scientific computing, machine learning, testing, and education. A Python program is commonly stored in a `.py` file and executed by the Python interpreter. The language supports procedural, object-oriented, and functional programming styles.

Python's readability does not remove the need for good engineering practices. Programs still need clear requirements, tests, logging, security review, and maintainable structure. A short script can become difficult to maintain when it grows without modules, documentation, or consistent naming.

## 2. Variables and types
A variable is a name referring to an object. Common built-in types include `int`, `float`, `str`, `bool`, `list`, `tuple`, `dict`, and `set`. Python is dynamically typed: a name can refer to objects of different types at different points, although predictable types make code easier to understand. Use descriptive names such as `student_count` rather than vague names such as `x`.

Strings represent text and support operations such as concatenation, slicing, and formatting. F-strings are a readable way to place values inside text: `f"Found {count} records"`. Numeric operations should account for the difference between integer division (`//`) and ordinary division (`/`). For money, consider `decimal.Decimal` when exact decimal arithmetic matters.

## 3. Conditions and loops
Conditional statements use `if`, `elif`, and `else`. A condition should express a clear business rule. For example, a booking system might check whether a requested checkout date is later than the check-in date before accepting a reservation. Loops include `for` and `while`. A `for` loop is often used to visit each item in a collection, while a `while` loop repeats while a condition remains true.

Avoid loops that never change their exit condition. Use `break` only when it makes the flow clearer, and use `continue` when skipping an item is the clearest action. List comprehensions can be concise, but ordinary loops are often easier to debug for complex operations.

## 4. Functions
A function packages a named operation. Functions can accept parameters and return results. A function should generally do one coherent job, use meaningful names, and avoid hidden changes to global state. Type hints document expected inputs and outputs; they help readers and tools, although Python does not enforce them automatically at runtime.

Default parameter values are evaluated once when the function is defined. Avoid mutable defaults such as `def add_item(item, items=[]):`. Prefer `None` and create a new list inside the function. This prevents calls from unexpectedly sharing the same list.

## 5. Classes and objects
A class defines data and behaviour; an instance is an object created from that class. Classes are useful when a domain concept has related state and operations. They are not required for every program. A simple data transformation may be clearer as a function. Composition, where an object contains other objects, is often easier to change than a deep inheritance hierarchy.

## 6. Environments and dependencies
A virtual environment isolates project dependencies from other Python projects. Create one with `python -m venv .venv`, activate it, and install dependencies with `pip`. Keep a dependency file so another developer can reproduce the setup. Do not commit local virtual environments, caches, secrets, or generated databases to source control.

## 7. Readability
PEP 8 provides widely used Python style conventions. Use four spaces for indentation, keep functions focused, and choose names that describe intent. Comments should explain why a decision exists, not repeat what an obvious line does. A README should describe the purpose, setup, commands, configuration, limitations, and examples.

## 8. Common beginner errors
A `NameError` usually means a name has not been defined in the current scope. A `TypeError` often indicates an operation received an incompatible type. An `IndexError` means a sequence index is outside its valid range. An `ImportError` indicates that a requested module or name could not be imported. Read the complete traceback, locate the final exception line, and inspect the relevant call rather than changing unrelated code at random.

## 9. Small example
A robust function for computing a simple average should handle empty input explicitly:
```python
def average(values: list[float]) -> float:
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)
```
Raising a clear exception makes the contract visible. A caller can decide whether to show an error message, request more data, or skip the calculation.

## 10. Practical checklist
Before sharing a Python project, confirm that the installation instructions work in a clean environment, required files are present, test commands are documented, user input is validated, and error messages are useful. Record known limitations honestly. A project that is easy to install and verify is more valuable than one that merely works on its creator's computer.


## 11. Iteration and generators
An iterator provides values one at a time. Generators, commonly written with `yield`, can produce sequences lazily instead of building the whole result in memory. This is useful for processing log files or streams. A generator can generally be consumed once, so code should not assume it can restart automatically. If multiple passes are needed, create a new generator or store the required values.

## 12. Dates and time
Date and time handling requires care around formats and timezones. Use standard date and time types rather than comparing display strings. A timestamp should have a clear timezone policy. For an application serving multiple regions, store a consistent representation and convert for display. Tests should include boundary dates, daylight-saving transitions where relevant, and invalid user input.

## 13. Data serialization
JSON is commonly used to exchange structured data between applications. Python's `json` module can encode and decode compatible values. Validate decoded content because valid JSON can still have the wrong shape or unsafe values. Do not use `eval` to parse untrusted text. For complex Python objects, define an explicit serialization format rather than relying on implementation details.
