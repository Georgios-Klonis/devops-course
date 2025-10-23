"""
Python Testing Fundamentals - Practical Exercise (Student Version)
===================================================================

This exercise covers:
1. Unit Testing with unittest and pytest
2. Integration Testing
3. Mocking external dependencies
4. Patching functions and methods

Setup:
------
pip install pytest pytest-mock requests --break-system-packages

Run tests:
----------
pytest testing_exercise_student.py -v
or
python -m pytest testing_exercise_student.py -v
"""

import requests
import json
from typing import List, Dict, Optional, Any
from datetime import datetime


# ============================================================================
# PART 1: Simple Functions for Unit Testing
# ============================================================================

def calculate_total_price(price: float, quantity: int, discount_percent: float = 0) -> float:
    """
    Calculate total price with optional discount.
    
    Args:
        price: Unit price
        quantity: Number of items
        discount_percent: Discount percentage (0-100)
    
    Returns:
        Total price after discount
    """
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")
    
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    subtotal = price * quantity
    discount_amount = subtotal * (discount_percent / 100)
    return subtotal - discount_amount


def validate_email(email: str) -> bool:
    """Simple email validation."""
    if not email or '@' not in email:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    username, domain = parts
    if not username or not domain or '.' not in domain:
        return False
    
    return True


# ============================================================================
# PART 2: Classes for Integration Testing
# ============================================================================

class Database:
    """Simulated database connection."""
    
    def __init__(self):
        self.data = {}
        self.connected = False
    
    def connect(self):
        """Simulate database connection."""
        self.connected = True
        return True
    
    def disconnect(self):
        """Simulate database disconnection."""
        self.connected = False
    
    def save(self, key: str, value: Any) -> bool:
        """Save data to database."""
        if not self.connected:
            raise ConnectionError("Database not connected")
        self.data[key] = value
        return True
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve data from database."""
        if not self.connected:
            raise ConnectionError("Database not connected")
        return self.data.get(key)


class UserRepository:
    """Repository for user operations."""
    
    def __init__(self, database: Database):
        self.db = database
    
    def create_user(self, user_id: str, name: str, email: str) -> Dict:
        """Create a new user."""
        if not validate_email(email):
            raise ValueError("Invalid email format")
        
        user = {
            'id': user_id,
            'name': name,
            'email': email,
            'created_at': datetime.now().isoformat()
        }
        
        self.db.save(f"user:{user_id}", user)
        return user
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Retrieve a user by ID."""
        return self.db.get(f"user:{user_id}")


# ============================================================================
# PART 3: External API Calls (for Mocking/Patching)
# ============================================================================

class WeatherService:
    """Service that calls external weather API."""
    
    def __init__(self, api_key: str = "demo"):
        self.api_key = api_key
        self.base_url = "https://api.weather.com"
    
    def get_temperature(self, city: str) -> float:
        """
        Fetch current temperature for a city.
        This makes a real API call - we'll mock this in tests!
        """
        response = requests.get(
            f"{self.base_url}/current",
            params={'city': city, 'key': self.api_key}
        )
        response.raise_for_status()
        data = response.json()
        return data['temperature']
    
    def is_good_weather(self, city: str) -> bool:
        """Determine if weather is good (above 20°C)."""
        temp = self.get_temperature(city)
        return temp > 20


class NotificationService:
    """Service for sending notifications."""
    
    @staticmethod
    def send_email(to: str, subject: str, body: str) -> bool:
        """
        Send an email notification.
        In reality, this would call an email service.
        """
        # Simulate email sending
        print(f"Sending email to {to}: {subject}")
        return True
    
    @staticmethod
    def send_sms(phone: str, message: str) -> bool:
        """Send SMS notification."""
        print(f"Sending SMS to {phone}: {message}")
        return True


class OrderProcessor:
    """Process orders with notifications and weather checks."""
    
    def __init__(self, weather_service: WeatherService, notification_service: NotificationService):
        self.weather_service = weather_service
        self.notification_service = notification_service
    
    def process_order(self, order_id: str, customer_email: str, city: str) -> Dict:
        """
        Process an order and send notification.
        Checks weather to add special message.
        """
        # Check weather
        is_good = self.weather_service.is_good_weather(city)
        
        # Prepare message
        message = f"Order {order_id} confirmed!"
        if is_good:
            message += " Enjoy the nice weather!"
        
        # Send notification
        sent = self.notification_service.send_email(
            customer_email,
            "Order Confirmation",
            message
        )
        
        return {
            'order_id': order_id,
            'notification_sent': sent,
            'weather_checked': True,
            'is_good_weather': is_good
        }


# ============================================================================
# TESTS START HERE
# ============================================================================

import pytest
from unittest import mock
from unittest.mock import Mock, MagicMock, patch, call


# ============================================================================
# EXERCISE 1: Basic Unit Tests
# ============================================================================

class TestCalculateTotalPrice:
    """Unit tests for calculate_total_price function."""
    
    def test_basic_calculation_no_discount(self):
        """Test basic price calculation without discount."""
        assert calculate_total_price(price=10.0, quantity=5) == 50
    
    def test_calculation_with_discount(self):
        """Test price calculation with discount."""
        assert calculate_total_price(price=100.0, quantity=2, discount_percent=10) == 180
    
    def test_calculation_with_50_percent_discount(self):
        """Test with 50% discount."""
        assert calculate_total_price(price=50.0, quantity=4, discount_percent=50) == 100
    
    def test_zero_quantity(self):
        """Test with zero quantity."""
        assert calculate_total_price(price=10.0, quantity=0) == 0
    
    def test_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            calculate_total_price(price=-10.0, quantity=5)
    
    def test_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            calculate_total_price(price=10.0, quantity=-5)
    
    def test_invalid_discount_over_100(self):
        """Test that discount over 100 raises ValueError."""
        with pytest.raises(ValueError, match="must be between 0 and 100"):
            calculate_total_price(price=10.0, quantity=5, discount_percent=101)
    
    def test_invalid_discount_negative(self):
        """Test that negative discount raises ValueError."""
        with pytest.raises(ValueError, match="must be between 0 and 100"):
            calculate_total_price(price=10.0, quantity=5, discount_percent=-101)


class TestValidateEmail:
    """Unit tests for email validation."""
    
    def test_valid_email(self):
        """Test valid email format."""
        assert validate_email(email="user@example.com")
    
    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        assert validate_email(email="user@mail.example.com")
    
    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        assert not validate_email(email="userexample.com")
    
    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        assert not validate_email(email="user@")
    
    def test_invalid_email_no_tld(self):
        """Test invalid email without TLD."""
        assert not validate_email(email="user@example")
    
    def test_invalid_email_empty(self):
        """Test empty email."""
        assert not validate_email(email="")
    
    def test_invalid_email_multiple_at(self):
        """Test email with multiple @ symbols."""
        assert not validate_email(email="user@@example.com")


# ============================================================================
# EXERCISE 2: Integration Tests
# ============================================================================

class TestUserRepositoryIntegration:
    """Integration tests for UserRepository with Database."""
    
    @pytest.fixture
    def database(self):
        """Create a database instance for testing."""
        db = Database()
        db.connect()
        yield db
        db.disconnect()
    
    @pytest.fixture
    def user_repo(self, database):
        """Create a UserRepository with connected database."""
        user_repo = UserRepository(database=database)

        return user_repo
    
    def test_create_and_retrieve_user(self, user_repo):
        """Test creating and retrieving a user (integration test)."""
        user = user_repo.create_user(
                    user_id="123", 
                    name="John Doe",
                    email="john@example.com"
                )
                
        assert  user["id"] == "123" and user["name"] == "John Doe" and user["email"] == "john@example.com" and user["created_at"] != None

        user = user_repo.get_user(user_id="123")

        assert user != None and user["id"] == "123" and user["name"] == "John Doe"
    
    def test_create_user_with_invalid_email(self, user_repo):
        """Test that creating user with invalid email raises error."""

        with pytest.raises(ValueError, match="Invalid email"):
            user_repo.create_user(
                user_id="123", 
                name="John Doe",
                email="invalid-email"
            )
    
    def test_get_nonexistent_user(self, user_repo):
        """Test retrieving a user that doesn't exist."""
        assert user_repo.get_user(user_id="999") == None
    
    def test_database_not_connected_raises_error(self):
        """Test that operations fail when database is not connected."""
        db = Database()

        user_repo = UserRepository(database=db) 

        with pytest.raises(ConnectionError, match="not connected"):
            user_repo.create_user(
                user_id="123", 
                name="John Doe",
                email="john@example.com"
            )


# ============================================================================
# EXERCISE 3: Mocking External Dependencies
# ============================================================================

class TestWeatherServiceMocking:
    """Tests demonstrating mocking of external API calls."""
    
    @patch('requests.get')
    def test_get_temperature_success(self, mock_get):
        """Test getting temperature with mocked API response."""
        mock_response = Mock()
        mock_response.json.return_value = {"temperature": 25.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response


        ws = WeatherService(api_key="test")

        assert ws.get_temperature(city="London") == 25.5

        mock_get.assert_called_once_with(
                    "https://api.weather.com/current",
                    params={"city": "London", "key": "test"},
                )
    
    @patch('requests.get')
    def test_is_good_weather_true(self, mock_get):
        """Test good weather detection (temp > 20)."""
        mock_response = Mock()
        mock_response.json.return_value = {"temperature": 25.0}
        mock_get.return_value = mock_response

        ws = WeatherService(api_key="test")

        assert ws.is_good_weather(city="Paris")
    
    @patch('requests.get')
    def test_is_good_weather_false(self, mock_get):
        """Test bad weather detection (temp <= 20)."""
        mock_response = Mock()
        mock_response.json.return_value = {"temperature": 10.0}
        mock_get.return_value = mock_response

        ws = WeatherService(api_key="test")

        assert not ws.is_good_weather(city="Berlin")
    
    @patch('requests.get')
    def test_api_error_handling(self, mock_get):
        """Test handling of API errors."""
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        ws = WeatherService(api_key="test")

        with pytest.raises(requests.exceptions.RequestException):
            ws.get_temperature("Tokyo")


# ============================================================================
# EXERCISE 4: Advanced Mocking and Patching
# ============================================================================

class TestOrderProcessorMocking:
    """Tests demonstrating complex mocking scenarios."""
    
    def test_process_order_with_good_weather(self):
        """Test order processing with mocked weather and notification services."""
        mock_weather = Mock(spec=WeatherService)
        mock_weather.is_good_weather.return_value = True

        mock_notification = Mock(spec=NotificationService)
        mock_notification.send_email.return_value = True

        processor = OrderProcessor(
            weather_service=mock_weather,
            notification_service=mock_notification,
        )

        result = processor.process_order(
            "ORD-001",
            "customer@example.com",
            "Madrid",
        )

        assert result["order_id"] == "ORD-001" and result["notification_sent"] is True and result["is_good_weather"] is True

        mock_weather.is_good_weather.assert_called_once_with("Madrid")
        mock_notification.send_email.assert_called_once_with(
            "customer@example.com",
            "Order Confirmation",
            mock.ANY,
        )
        assert "Enjoy the nice weather" in mock_notification.send_email.call_args.args[2]

    
    def test_process_order_with_bad_weather(self):
        """Test order processing with bad weather."""
        mock_weather = Mock(spec=WeatherService)
        mock_weather.is_good_weather.return_value = False

        mock_notification = Mock(spec=NotificationService)
        mock_notification.send_email.return_value = True

        processor = OrderProcessor(
            weather_service=mock_weather,
            notification_service=mock_notification,
        )

        result = processor.process_order(
            "ORD-002",
            "customer@example.com",
            "Oslo",
        )

        assert result["is_good_weather"] is False

        mock_notification.send_email.assert_called_once_with(
            "customer@example.com",
            "Order Confirmation",
            mock.ANY,
        )
        assert "Enjoy the nice weather" not in mock_notification.send_email.call_args.args[2]

    
    @patch.object(NotificationService, "send_email")
    @patch.object(WeatherService, "is_good_weather")
    def test_process_order_with_patch_object(self, mock_weather, mock_email):
        """Test using patch.object decorator."""
        mock_weather.return_value = True
        mock_email.return_value = True

        weather = WeatherService(api_key="dummy")
        notification = NotificationService()
        processor = OrderProcessor(weather, notification)

        result = processor.process_order(
            "ORD-003",
            "test@example.com",
            "Barcelona",
        )

        assert result["notification_sent"] is True

        mock_weather.assert_called_once_with("Barcelona")
        mock_email.assert_called_once_with(
            "test@example.com",
            "Order Confirmation",
            "Order ORD-003 confirmed! Enjoy the nice weather!",
        )

    
    def test_notification_failure_handling(self):
        """Test handling notification service failures."""
        mock_weather = Mock(spec=WeatherService)
        mock_weather.is_good_weather.return_value = True

        mock_notification = Mock(spec=NotificationService)
        mock_notification.send_email.return_value = False

        processor = OrderProcessor(
            weather_service=mock_weather,
            notification_service=mock_notification,
        )

        result = processor.process_order(
            "ORD-004",
            "alert@example.com",
            "Lisbon",
        )

        assert result["notification_sent"] is False


# ============================================================================
# EXERCISE 5: Pytest Fixtures and Parametrize
# ============================================================================

class TestPytestFeatures:
    """Demonstrate pytest-specific features."""
    
    @pytest.fixture
    def sample_prices(self):
        """Fixture providing sample price data."""
        return [
            (10.0, 5, 0, 50.0),
            (10.0, 5, 10, 45.0),
            (100.0, 2, 25, 150.0),
        ]
    
    @pytest.mark.parametrize("price,quantity,discount,expected", [
        (10.0, 5, 0, 50.0),
        (10.0, 5, 10, 45.0),
        (100.0, 2, 25, 150.0),
        (50.0, 10, 20, 400.0),
        (25.0, 4, 50, 50.0),
    ])
    def test_calculate_total_price_parametrized(self, price, quantity, discount, expected):
        """Test multiple scenarios using parametrize."""
        result = calculate_total_price(price=price, quantity=quantity, discount_percent=discount)
        assert result == expected

    
    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("test@mail.example.org", True),
        ("invalid", False),
        ("no-at-sign.com", False),
        ("@example.com", False),
        ("user@", False),
        ("", False),
    ])
    def test_validate_email_parametrized(self, email, expected):
        """Test email validation with multiple cases."""
        result = validate_email(email)
        assert result == expected



# ============================================================================
# BONUS: Mock Best Practices Examples
# ============================================================================

class TestMockBestPractices:
    """Examples of best practices when using mocks."""
    
    def test_using_spec_prevents_invalid_attributes(self):
        """Using spec prevents accessing non-existent attributes."""
        mock_weather = Mock(spec=WeatherService)
        mock_weather.get_temperature.return_value = 20.0

        assert mock_weather.get_temperature("Athens") == 20.0

        with pytest.raises(AttributeError):
            mock_weather.non_existent_method()

    
    def test_verify_exact_calls_with_assert_called_with(self):
        """Verify exact arguments passed to mocked method."""
        mock_notification = Mock()
        mock_notification.send_email("test@example.com", "Subject", "Body")

        mock_notification.send_email.assert_called_with(
            "test@example.com",
            "Subject",
            "Body",
        )

    
    def test_verify_call_count(self):
        """Verify how many times a mock was called."""
        mock_service = Mock()

        mock_service.some_method()
        mock_service.some_method()
        mock_service.some_method()

        assert mock_service.some_method.call_count == 3


    def test_mock_side_effects(self):
        """Use side_effect for exceptions or varying returns."""
        mock_api = Mock()
        mock_api.fetch.side_effect = [10, 20, 30]

        first = mock_api.fetch()
        second = mock_api.fetch()
        third = mock_api.fetch()

        assert first == 10
        assert second == 20
        assert third == 30


    def test_reset_mock(self):
        """Reset a mock to clear call history."""
        mock_service = Mock()

        mock_service.method()
        assert mock_service.method.called is True

        mock_service.reset_mock()
        assert mock_service.method.called is False


if __name__ == "__main__":
    print("Run tests with: pytest testing_exercise_student.py -v")
    print("\nOr with coverage: pytest testing_exercise_student.py -v --cov")
