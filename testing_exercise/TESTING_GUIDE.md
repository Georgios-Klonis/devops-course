# Python Testing Fundamentals - Study Guide

## Overview
This guide accompanies `testing_exercise.py` and will help you understand testing concepts through hands-on practice.

## Setup Instructions

1. **Install required packages:**
```bash
pip install pytest pytest-mock requests --break-system-packages
```

2. **Run all tests:**
```bash
pytest testing_exercise.py -v
```

3. **Run specific test class:**
```bash
pytest testing_exercise.py::TestCalculateTotalPrice -v
```

4. **Run with coverage:**
```bash
pytest testing_exercise.py --cov --cov-report=html
```

---

## Part 1: Unit Testing Fundamentals

### What is Unit Testing?
Unit testing tests individual components (functions, methods) in isolation. Each test should:
- Test ONE specific behavior
- Be independent of other tests
- Run quickly
- Have clear pass/fail criteria

### Key Concepts in the Exercise:

#### 1. **Basic Assertions**
```python
def test_basic_calculation_no_discount(self):
    result = calculate_total_price(10.0, 5)
    assert result == 50.0
```
- Uses simple `assert` statements
- Tests expected vs actual values

#### 2. **Testing Exceptions**
```python
def test_negative_price_raises_error(self):
    with pytest.raises(ValueError, match="must be non-negative"):
        calculate_total_price(-10.0, 5)
```
- Verifies that code raises expected exceptions
- Can check exception message with `match` parameter

#### 3. **Test Organization**
- Group related tests in classes
- Use descriptive test names that explain what they test
- Follow naming convention: `test_<what_is_being_tested>`

### Practice Tasks:

**Task 1.1:** Add a new test case for `calculate_total_price` that tests:
- A 100% discount (should return 0)

**Task 1.2:** Write a new function `calculate_discount_amount(price, quantity, discount_percent)` that returns only the discount amount, then write 3 unit tests for it.

**Task 1.3:** Add edge case tests for `validate_email`:
- Email with special characters (e.g., "user+tag@example.com")
- Email with numbers (e.g., "user123@example.com")

---

## Part 2: Integration Testing

### What is Integration Testing?
Integration tests verify that multiple components work together correctly. They test:
- Interactions between classes/modules
- Data flow through the system
- Real dependencies (or realistic test doubles)

### Key Concepts:

#### 1. **Pytest Fixtures**
```python
@pytest.fixture
def database(self):
    db = Database()
    db.connect()
    yield db
    db.disconnect()
```
- Fixtures provide reusable test data/objects
- `yield` allows setup and teardown
- Automatically passed to tests that need them

#### 2. **Testing Component Interactions**
```python
def test_create_and_retrieve_user(self, user_repo):
    user = user_repo.create_user("123", "John Doe", "john@example.com")
    retrieved = user_repo.get_user("123")
    assert retrieved['id'] == "123"
```
- Tests that `UserRepository` and `Database` work together
- Verifies data persists correctly

#### 3. **Testing Error Propagation**
```python
def test_database_not_connected_raises_error(self):
    db = Database()  # Not connected
    repo = UserRepository(db)
    with pytest.raises(ConnectionError):
        repo.create_user("125", "Test User", "test@example.com")
```
- Ensures errors are handled correctly across components

### Practice Tasks:

**Task 2.1:** Add a method `update_user(user_id, **kwargs)` to `UserRepository` and write integration tests for it.

**Task 2.2:** Create a fixture that pre-populates the database with 3 users and write a test that retrieves all of them.

**Task 2.3:** Write a test that verifies the database properly disconnects and subsequent operations fail.

---

## Part 3: Mocking External Dependencies

### What is Mocking?
Mocking replaces real objects with test doubles that simulate behavior. Use mocks to:
- Avoid external API calls
- Control test conditions
- Speed up tests
- Test error scenarios

### Key Concepts:

#### 1. **Basic Mock Creation**
```python
mock_weather = Mock(spec=WeatherService)
mock_weather.is_good_weather.return_value = True
```
- `Mock()` creates a mock object
- `spec=` ensures only real methods can be called
- `return_value` sets what the method returns

#### 2. **Patching with Decorators**
```python
@patch('requests.get')
def test_get_temperature_success(self, mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {'temperature': 25.5}
    mock_get.return_value = mock_response
```
- `@patch` replaces a module/function temporarily
- Decorator adds mock as test parameter
- Allows testing without real API calls

#### 3. **Verifying Mock Calls**
```python
mock_get.assert_called_once_with(
    "https://api.weather.com/current",
    params={'city': 'London', 'key': 'test'}
)
```
- Verify the mock was called with expected arguments
- Ensures your code calls dependencies correctly

### Common Mock Methods:
- `assert_called()` - was it called?
- `assert_called_once()` - called exactly once?
- `assert_called_with(*args, **kwargs)` - called with these args?
- `assert_not_called()` - was never called?
- `call_count` - how many times called?
- `call_args` - get the arguments from the last call

### Practice Tasks:

**Task 3.1:** Create a `StockPriceService` class that fetches stock prices from an API. Write tests that mock the API responses.

**Task 3.2:** Write a test for `WeatherService.get_temperature` that simulates an HTTP timeout error.

**Task 3.3:** Add verification that checks the exact URL and parameters used in the API call.

---

## Part 4: Advanced Patching Techniques

### What is Patching?
Patching temporarily replaces objects in code during testing. It's more powerful than basic mocking.

### Key Concepts:

#### 1. **patch.object()**
```python
@patch.object(NotificationService, 'send_email')
def test_with_patch_object(self, mock_email):
    mock_email.return_value = True
```
- Patches a specific method on a class
- Useful for static methods and class methods

#### 2. **Multiple Patches**
```python
@patch.object(NotificationService, 'send_email')
@patch.object(WeatherService, 'is_good_weather')
def test_process_order_with_patch_object(self, mock_weather, mock_email):
```
- Stack decorators for multiple patches
- Parameters appear in reverse order (bottom-to-top)

#### 3. **Context Manager Patching**
```python
with patch('module.function') as mock_func:
    mock_func.return_value = "test"
    # use mock within this block
```
- Alternative to decorator syntax
- Useful for patching only part of a test

#### 4. **Mock Side Effects**
```python
mock_api.fetch.side_effect = [10, 20, 30]  # Different returns
mock_api.fetch.side_effect = Exception("Error")  # Raise error
```
- Control multiple calls
- Simulate failures

### Practice Tasks:

**Task 4.1:** Create a `PaymentProcessor` class that calls both a payment gateway API and sends confirmation emails. Write tests that mock both dependencies.

**Task 4.2:** Write a test where the first API call fails but a retry succeeds (use `side_effect` with a list).

**Task 4.3:** Use context manager patching instead of decorators for one of the existing tests.

---

## Part 5: Pytest Advanced Features

### 1. **Parametrized Tests**
Run the same test with different inputs:
```python
@pytest.mark.parametrize("price,quantity,discount,expected", [
    (10.0, 5, 0, 50.0),
    (10.0, 5, 10, 45.0),
    (100.0, 2, 25, 150.0),
])
def test_calculate_total_price_parametrized(self, price, quantity, discount, expected):
    result = calculate_total_price(price, quantity, discount)
    assert result == expected
```

**Benefits:**
- Reduces code duplication
- Easy to add more test cases
- Clear test data

### 2. **Fixture Scopes**
```python
@pytest.fixture(scope="module")  # Run once per module
@pytest.fixture(scope="class")   # Run once per class
@pytest.fixture(scope="function") # Run for each test (default)
@pytest.fixture(scope="session")  # Run once per test session
```

### 3. **Markers**
```python
@pytest.mark.slow  # Custom marker
@pytest.mark.skip(reason="Not implemented yet")
@pytest.mark.skipif(condition, reason="...")
@pytest.mark.xfail(reason="Known bug")
```

Run specific markers:
```bash
pytest -m slow  # Run only tests marked as slow
pytest -m "not slow"  # Run all except slow tests
```

### Practice Tasks:

**Task 5.1:** Convert the `TestValidateEmail` tests to use `@pytest.mark.parametrize`.

**Task 5.2:** Create a fixture with `scope="module"` that creates a database connection used by all tests in a class.

**Task 5.3:** Add a custom marker `@pytest.mark.api` to tests that mock external APIs.

---

## Common Pitfalls to Avoid

1. **Testing implementation details instead of behavior**
   - Bad: Testing internal variable names
   - Good: Testing output/behavior

2. **Tests that depend on each other**
   - Bad: test_2 requires test_1 to run first
   - Good: Each test is independent

3. **Over-mocking**
   - Bad: Mocking everything including simple functions
   - Good: Only mock external dependencies

4. **Not testing error cases**
   - Bad: Only testing happy path
   - Good: Test both success and failure scenarios

5. **Unclear test names**
   - Bad: `test_1`, `test_function`
   - Good: `test_calculate_total_with_discount_returns_correct_amount`

---

## Running Tests - Quick Reference

```bash
# Run all tests
pytest testing_exercise.py -v

# Run specific test class
pytest testing_exercise.py::TestCalculateTotalPrice -v

# Run specific test
pytest testing_exercise.py::TestCalculateTotalPrice::test_basic_calculation_no_discount -v

# Run with coverage
pytest testing_exercise.py --cov --cov-report=html

# Run tests matching a pattern
pytest testing_exercise.py -k "email" -v

# Run tests with specific marker
pytest testing_exercise.py -m "parametrize" -v

# Show print statements
pytest testing_exercise.py -v -s

# Stop on first failure
pytest testing_exercise.py -x

# Run last failed tests
pytest testing_exercise.py --lf
```

---

## Additional Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **unittest.mock Documentation**: https://docs.python.org/3/library/unittest.mock.html
- **Testing Best Practices**: https://docs.pytest.org/en/stable/goodpractices.html

## Next Steps

1. Run all the tests and make sure they pass
2. Read through each test to understand what it does
3. Complete the practice tasks in each section
4. Try the extended challenges
5. Apply these concepts to your own projects!

Good luck with your testing journey!
