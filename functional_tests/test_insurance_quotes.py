import pytest
import requests

API_URL = "http://localhost:5312/api/insurance-quote"


@pytest.mark.parametrize(
    "scenario, payload",
    [

        ("Valid request with business use",
         {"proposer": "John Doe", "vehicle_registration": "AB123CD", "is_business_use": True}),

        ("Valid request without business use", {"proposer": "Alice", "vehicle_registration": "XYZ987"}),

        ("Minimum length proposer and vehicle_registration", {"proposer": "A", "vehicle_registration": "A"}),

        ("Maximum length proposer and vehicle_registration", {"proposer": "A" * 50, "vehicle_registration": "X" * 10}),

        ("Valid request with explicit false business use",
         {"proposer": "John Doe", "vehicle_registration": "AB123CD", "is_business_use": False}),

        ("Valid request with proposer wrapped with whitespaces",
         {"proposer": " Alice\t\r\n ", "vehicle_registration": "XYZ987"}),

        ("Valid request with vehicle_registration wrapped with whitespaces",
         {"proposer": "Alice", "vehicle_registration": " XYZ987 \r\t\n"}),

    ],
)
async def test_insurance_quote_positive(scenario, payload, async_db_connection):
    response = requests.post(API_URL, json=payload)
    assert response.status_code == 200

    record_json = response.json()
    record_id = record_json['id']
    # assert record in the database
    result = await async_db_connection.fetchrow(
        "SELECT * FROM insurance_quote WHERE id=$1",
        record_id
    )
    assert result['vehicle_registration'] == payload['vehicle_registration'].strip()
    assert result['proposer'] == payload['proposer'].strip()
    assert result['is_business_use'] == (True if payload.get('is_business_use') else False)
    assert result['quote_amount'] > 0
    assert result['agent_discount_amount'] > 0
    assert result['agent_notes'] is not None
    assert result['quote_date'] is not None

    request_id = response.headers['request-id']
    assert request_id is not None


@pytest.mark.parametrize(
    "scenario, payload, expected_status, expected_error",
    [

        ("Missing proposer", {"vehicle_registration": "AB123CD", "is_business_use": True}, 422, "proposer is required"),

        ("Missing vehicle_registration", {"proposer": "John Doe", "is_business_use": False}, 422,
         "vehicle_registration is required"),

        ("Empty proposer", {"proposer": "", "vehicle_registration": "AB123CD"}, 422,
         "proposer must be between 1 and 50 characters"),

        ("Empty vehicle_registration", {"proposer": "John Doe", "vehicle_registration": ""}, 422,
         "vehicle_registration must be between 1 and 10 characters"),

        ("Whitespace proposer", {"proposer": " ", "vehicle_registration": "AB123CD"}, 422,
         "proposer must be between 1 and 50 characters"),

        ("Whitespace vehicle_registration", {"proposer": "John Doe", "vehicle_registration": " "}, 422,
         "vehicle_registration must be between 1 and 10 characters"),

        ("Proposer exceeds max length", {"proposer": "A" * 51, "vehicle_registration": "AB123CD"}, 422,
         "proposer must be between 1 and 50 characters"),

        ("Vehicle registration exceeds max length", {"proposer": "John Doe", "vehicle_registration": "X" * 11}, 422,
         "vehicle_registration must be between 1 and 10 characters"),

        ("Invalid is_business_use type",
         {"proposer": "John Doe", "vehicle_registration": "AB123CD", "is_business_use": "yes"}, 422,
         "Input should be a valid boolean"),

        ("Proposer with only spaces", {"proposer": "      ", "vehicle_registration": "AB123CD"}, 422,
         "proposer must be between 1 and 50 characters"),

        ("Vehicle registration with only spaces", {"proposer": "John Doe", "vehicle_registration": "      "}, 422,
         "vehicle_registration must be between 1 and 10 characters"),
    ],
)
def test_insurance_quote_negative(scenario, payload, expected_status, expected_error):
    response = requests.post(API_URL, json=payload)
    assert response.status_code == expected_status, f"{scenario} failed: Expected {expected_status}, got {response.status_code}"

    detail = response.json()
    assert expected_error in str(detail), f"{scenario} failed: Expected error message '{expected_error}'"

    request_id = response.headers['request-id']
    assert request_id is not None

