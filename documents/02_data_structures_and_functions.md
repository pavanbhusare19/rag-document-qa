# Data Structures, Algorithms, and Functions

## 1. Lists and tuples
A list is an ordered, mutable collection. It is appropriate when elements may be added, removed, or updated. A tuple is ordered but immutable, making it useful for fixed groups of values. Both can contain mixed types, but consistent element types usually improve clarity. List operations such as appending are convenient; repeatedly inserting at the beginning can be expensive for large lists.

## 2. Dictionaries and sets
A dictionary stores key-value mappings. It is useful for looking up a student's record by an identifier or grouping configuration settings by name. Keys should be hashable and are commonly strings or numbers. A set stores unique elements and supports efficient membership checks in typical cases. For example, a set can identify duplicate email addresses during a validation pass.

Dictionary access with `mapping[key]` raises `KeyError` if the key is absent. Use `mapping.get(key)` when a missing key is an expected situation, or explicitly validate required keys when absence is an error. Do not silently substitute a default for a required value if that could hide corrupted data.

## 3. Choosing a structure
Choose a data structure based on the operations that matter. Lists are natural for preserving order. Dictionaries are suitable for key-based retrieval. Sets help with uniqueness and membership. A queue processes items in first-in, first-out order; a stack processes items in last-in, first-out order. A heap can efficiently expose the smallest or largest priority item.

The best choice depends on input size, update patterns, ordering requirements, and code readability. Measure real workloads before optimizing. A theoretically faster algorithm can be slower in a particular implementation due to overhead or small input sizes.

## 4. Algorithmic complexity
Big-O notation describes how resource use grows as input size increases. A single pass through `n` elements is commonly O(n). Nested loops over the same collection can be O(n²). Binary search on a sorted sequence is O(log n), because it halves the remaining search range each step. Sorting comparison-based data is typically O(n log n).

Complexity is not a substitute for testing. It describes growth, not exact execution time, memory use, or constant factors. Consider both time and space complexity when a system must handle large data or run on constrained devices.

## 5. Searching
Linear search checks elements one by one and works on unsorted data. Binary search requires sorted data and repeatedly narrows the search interval. If data changes frequently, the cost of maintaining sorted order may outweigh the search benefit. Always document assumptions such as whether IDs are unique and whether the input is sorted.

## 6. Sorting and stable ordering
Sorting puts items into an order defined by a key. In Python, `sorted(records, key=lambda row: row["score"])` returns a new list. `list.sort()` changes a list in place. Python's sort is stable, so equal-key items preserve their prior relative order. For multiple sort criteria, use a tuple key or a sequence of stable sorts.

## 7. Functional decomposition
Break a workflow into steps with named functions: parse input, validate records, transform data, save results, and report errors. Each function should have a clear contract. A useful contract specifies accepted inputs, returned values, side effects, and possible exceptions. Smaller functions make unit testing more targeted.

Avoid copying the same complex rule into several functions. Put the rule in one function and reuse it. This prevents one screen or API endpoint from behaving differently from another after a later change.

## 8. Defensive input validation
External input should be treated as untrusted. Check required fields, type, length, allowed values, and boundary conditions. For example, a quantity may need to be a positive integer and a date range must have a valid order. Validation should happen at the application boundary, even if a frontend already checks the same data.

Validation messages should be actionable and should not expose internal stack traces or secrets. Logs can include a request identifier and safe diagnostic information, but should avoid passwords, access tokens, and unnecessary personal data.

## 9. Example: duplicate detection
A simple duplicate check can use a set:
```python
seen = set()
duplicates = []
for value in values:
    if value in seen:
        duplicates.append(value)
    else:
        seen.add(value)
```
This preserves repeated occurrences in the `duplicates` output after the first appearance. If only unique duplicate values are required, collect them in another set. State the intended behaviour before writing the algorithm.

## 10. Review questions
When selecting a structure, ask: Do I need order? Can values change? Do I need unique items? Is lookup by key frequent? Is the collection large? What should happen for missing data? These questions help avoid choosing a structure merely because it is familiar.


## 11. Recursion
A recursive function calls itself to solve a smaller version of a problem. It needs a base case and progress toward that base case. Without either, it may recurse until Python raises a recursion error. Iteration is often more memory-efficient for simple repeated operations. Choose recursion when it makes a tree or divide-and-conquer algorithm clearer.

## 12. Graphs and trees
A tree is a hierarchical structure with nodes and edges. A graph represents relationships and may be directed or undirected. Breadth-first search explores nearby nodes first and commonly uses a queue. Depth-first search explores a path before backtracking and can use recursion or an explicit stack. Track visited nodes to avoid repeatedly exploring cycles.

## 13. Testing algorithm boundaries
Algorithm tests should include empty input, one item, duplicate values, already sorted values, reverse-sorted values, and values at domain boundaries. Randomized tests can reveal edge cases, but fixed seeds make failures easier to reproduce. For performance-sensitive code, test realistic sizes rather than only tiny examples.
