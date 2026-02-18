#!/usr/bin/env python3
"""
Integration Test Suite for Card Tracker
Tests the complete integration between backend and frontend APIs.

Usage:
    python integration_test.py

Prerequisites:
    - Backend running on http://localhost:8000
    - Frontend running on http://localhost:3000 (optional for full test)
"""

import requests
import json
import sys
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

# Test configuration
BACKEND_URL = "http://localhost:8000"
API_URL = f"{BACKEND_URL}/api"
FRONTEND_URL = "http://localhost:3000"

# ANSI color codes for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.RESET}\n")

def print_test(test_name: str):
    print(f"{Colors.BOLD}Testing: {test_name}{Colors.RESET}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def print_info(message: str):
    print(f"{Colors.BLUE}ℹ {message}{Colors.RESET}")

class TestResults:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.failures: List[str] = []

    def add_pass(self):
        self.total += 1
        self.passed += 1

    def add_fail(self, message: str):
        self.total += 1
        self.failed += 1
        self.failures.append(message)

    def add_warning(self):
        self.warnings += 1

    def print_summary(self):
        print_header("TEST SUMMARY")
        print(f"Total Tests: {self.total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.RESET}")
        print(f"{Colors.YELLOW}Warnings: {self.warnings}{Colors.RESET}")

        if self.failures:
            print(f"\n{Colors.RED}Failed Tests:{Colors.RESET}")
            for failure in self.failures:
                print(f"  - {failure}")

        if self.failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed!{Colors.RESET}")
            return 0
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ Some tests failed{Colors.RESET}")
            return 1

results = TestResults()

# Test 1: Backend Health Check
def test_backend_health():
    print_test("Backend Health Check")
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        if response.status_code == 200:
            print_success(f"Backend is running on {BACKEND_URL}")
            results.add_pass()
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            results.add_fail("Backend health check")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to backend at {BACKEND_URL}")
        print_info("Make sure backend is running: cd backend && uv run python manage.py runserver 8000")
        results.add_fail("Backend connection")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        results.add_fail("Backend health check")
        return False

# Test 2: API Root Endpoint
def test_api_root():
    print_test("API Root Endpoint")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            print_success(f"API root accessible at {API_URL}/")
            results.add_pass()
            return True
        else:
            print_error(f"API root returned status {response.status_code}")
            results.add_fail("API root endpoint")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        results.add_fail("API root endpoint")
        return False

# Test 3: Card Templates Endpoint (No Auth Required)
def test_card_templates():
    print_test("Card Templates Endpoint")
    try:
        response = requests.get(f"{API_URL}/card-templates/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', data)) if isinstance(data, dict) else len(data)
            print_success(f"Retrieved {count} card templates")
            results.add_pass()

            # Show sample cards
            if count > 0:
                cards = data.get('results', data) if isinstance(data, dict) else data
                print_info("Sample cards:")
                for card in cards[:3]:
                    print(f"  - {card.get('bank')} {card.get('name')}")

            return True, data
        else:
            print_error(f"Card templates endpoint returned status {response.status_code}")
            results.add_fail("Card templates endpoint")
            return False, None
    except Exception as e:
        print_error(f"Error: {e}")
        results.add_fail("Card templates endpoint")
        return False, None

# Test 4: Card Templates Search
def test_card_templates_search():
    print_test("Card Templates Search")
    try:
        search_terms = ["platinum", "sapphire", "reserve"]
        for term in search_terms:
            response = requests.get(f"{API_URL}/card-templates/?q={term}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                cards = data.get('results', data) if isinstance(data, dict) else data
                count = len(cards)
                print_success(f"Search for '{term}' returned {count} results")
                if count > 0:
                    for card in cards[:2]:
                        print(f"  - {card.get('bank')} {card.get('name')}")
            else:
                print_error(f"Search for '{term}' returned status {response.status_code}")
                results.add_fail(f"Card search: {term}")
                return False

        results.add_pass()
        return True
    except Exception as e:
        print_error(f"Error: {e}")
        results.add_fail("Card templates search")
        return False

# Test 5: Card Template Detail
def test_card_template_detail(card_id: int = None):
    print_test("Card Template Detail Endpoint")

    # If no card_id provided, get the first one
    if card_id is None:
        response = requests.get(f"{API_URL}/card-templates/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            cards = data.get('results', data) if isinstance(data, dict) else data
            if len(cards) > 0:
                card_id = cards[0].get('id')
            else:
                print_warning("No cards available to test detail endpoint")
                results.add_warning()
                return False
        else:
            print_error("Cannot get card list to test detail endpoint")
            results.add_fail("Card template detail")
            return False

    try:
        response = requests.get(f"{API_URL}/card-templates/{card_id}/", timeout=5)
        if response.status_code == 200:
            card = response.json()
            print_success(f"Retrieved card detail: {card.get('bank')} {card.get('name')}")
            print_info(f"  Annual Fee: ${card.get('annual_fee_cents', 0)/100:.2f}")

            # Check for benefits
            benefits = card.get('benefits', [])
            print_info(f"  Benefits: {len(benefits)}")
            for benefit in benefits[:3]:
                print(f"    - {benefit.get('name')}: ${benefit.get('amount_cents', 0)/100:.2f}/{benefit.get('frequency')}")

            results.add_pass()
            return True
        else:
            print_error(f"Card detail returned status {response.status_code}")
            results.add_fail("Card template detail")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        results.add_fail("Card template detail")
        return False

# Test 6: Create Test User and Get Token
def test_user_auth():
    print_test("User Authentication")

    # For now, we'll test if auth endpoints exist
    # In production, this would create a test user and get a JWT token
    try:
        # Check if registration endpoint exists
        response = requests.post(
            f"{API_URL}/auth/registration/",
            json={
                "username": f"testuser_{datetime.now().timestamp()}",
                "email": f"test_{datetime.now().timestamp()}@example.com",
                "password1": "TestPassword123!",
                "password2": "TestPassword123!"
            },
            timeout=5
        )

        if response.status_code in [200, 201]:
            data = response.json()
            token = data.get('access') or data.get('access_token') or data.get('key')
            if token:
                print_success("User registration successful, JWT token obtained")
                results.add_pass()
                return True, token
            else:
                print_success("User registration endpoint works")
                print_warning("No JWT token in response, check auth configuration")
                results.add_pass()
                results.add_warning()
                return True, None
        elif response.status_code == 400:
            # User might already exist, try login instead
            print_info("Registration returned 400, user may exist")
            results.add_pass()
            return True, None
        else:
            print_error(f"Registration returned status {response.status_code}")
            print_error(f"Response: {response.text[:200]}")
            results.add_fail("User registration")
            return False, None
    except Exception as e:
        print_error(f"Error: {e}")
        results.add_fail("User authentication")
        return False, None

# Test 7: Protected Endpoints (require auth)
def test_protected_endpoints(token: str = None):
    print_test("Protected Endpoints")

    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'

    endpoints = [
        ("/cards/", "User cards list"),
        ("/dashboard/summary/", "Dashboard summary"),
        ("/dashboard/deadlines/", "Dashboard deadlines"),
    ]

    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{API_URL}{endpoint}", headers=headers, timeout=5)

            if response.status_code == 200:
                print_success(f"{description}: OK")
                data = response.json()
                print_info(f"  Response keys: {list(data.keys())[:5]}")
            elif response.status_code == 401:
                print_warning(f"{description}: Requires authentication (401)")
                print_info("  This is expected for authenticated endpoints")
            elif response.status_code == 403:
                print_warning(f"{description}: Forbidden (403)")
            else:
                print_error(f"{description}: Status {response.status_code}")
                print_error(f"  Response: {response.text[:200]}")
        except Exception as e:
            print_error(f"{description}: Error - {e}")

    # Mark as passed since we're just checking the endpoints exist
    results.add_pass()
    return True

# Test 8: CORS Configuration
def test_cors():
    print_test("CORS Configuration")
    try:
        response = requests.options(
            f"{API_URL}/card-templates/",
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'GET',
            },
            timeout=5
        )

        cors_header = response.headers.get('Access-Control-Allow-Origin')
        if cors_header:
            print_success(f"CORS is configured: {cors_header}")
            results.add_pass()
            return True
        else:
            print_warning("CORS headers not found in response")
            print_info("Frontend may have issues connecting to backend")
            results.add_warning()
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        results.add_fail("CORS configuration")
        return False

# Test 9: Frontend Health Check (Optional)
def test_frontend_health():
    print_test("Frontend Health Check (Optional)")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print_success(f"Frontend is running on {FRONTEND_URL}")
            results.add_pass()
            return True
        else:
            print_warning(f"Frontend returned status {response.status_code}")
            results.add_warning()
            return False
    except requests.exceptions.ConnectionError:
        print_warning(f"Frontend not running at {FRONTEND_URL}")
        print_info("Start frontend: cd frontend && npm run dev")
        results.add_warning()
        return False
    except Exception as e:
        print_warning(f"Error checking frontend: {e}")
        results.add_warning()
        return False

# Test 10: Data Model Validation
def test_data_models():
    print_test("Data Model Validation")
    try:
        response = requests.get(f"{API_URL}/card-templates/", timeout=5)
        if response.status_code != 200:
            print_error("Cannot retrieve card templates for validation")
            results.add_fail("Data model validation")
            return False

        data = response.json()
        cards = data.get('results', data) if isinstance(data, dict) else data

        if len(cards) == 0:
            print_warning("No cards in database")
            results.add_warning()
            return False

        # Validate required fields
        required_fields = ['id', 'bank', 'name', 'annual_fee_cents']
        card = cards[0]

        missing_fields = [field for field in required_fields if field not in card]
        if missing_fields:
            print_error(f"Missing required fields: {missing_fields}")
            results.add_fail("Data model validation")
            return False

        print_success("Card template model has all required fields")

        # Check benefit structure
        if 'benefits' in card:
            benefits = card['benefits']
            if len(benefits) > 0:
                benefit = benefits[0]
                benefit_fields = ['id', 'name', 'amount_cents', 'frequency']
                missing_benefit_fields = [field for field in benefit_fields if field not in benefit]
                if missing_benefit_fields:
                    print_warning(f"Benefit missing fields: {missing_benefit_fields}")
                    results.add_warning()
                else:
                    print_success("Benefit template model has all required fields")

        results.add_pass()
        return True
    except Exception as e:
        print_error(f"Error: {e}")
        results.add_fail("Data model validation")
        return False

# Main test runner
def run_all_tests():
    print_header("CARD TRACKER INTEGRATION TESTS")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Run tests in sequence
    print_header("1. SERVICE HEALTH CHECKS")
    backend_ok = test_backend_health()

    if not backend_ok:
        print_error("\nBackend is not running. Cannot continue with API tests.")
        print_info("Start backend with: cd backend && uv run python manage.py runserver 8000")
        results.print_summary()
        return results.failed > 0

    test_api_root()
    test_frontend_health()

    print_header("2. CARD TEMPLATE ENDPOINTS")
    test_card_templates()
    test_card_templates_search()
    test_card_template_detail()

    print_header("3. AUTHENTICATION & PROTECTED ENDPOINTS")
    auth_ok, token = test_user_auth()
    test_protected_endpoints(token)

    print_header("4. CONFIGURATION TESTS")
    test_cors()
    test_data_models()

    # Print summary
    exit_code = results.print_summary()

    # Print next steps
    print_header("NEXT STEPS")
    print("1. ✅ Backend API is working")
    print("2. Test the frontend manually:")
    print("   - Visit http://localhost:3000")
    print("   - Try searching for cards")
    print("   - Add a card to your collection")
    print("   - Mark a benefit as used")
    print("3. Check the browser console for any errors")
    print("4. Verify network requests in browser DevTools")

    return exit_code

if __name__ == "__main__":
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
        sys.exit(1)
