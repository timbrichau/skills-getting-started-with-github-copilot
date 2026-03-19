def test_get_activities_returns_200(client):
    # Arrange — client is ready, no preconditions needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_count = 9

    # Act
    response = client.get("/activities")

    # Assert
    assert len(response.json()) == expected_count


def test_get_activities_contains_chess_club(client):
    # Arrange — Chess Club is part of the seed data

    # Act
    response = client.get("/activities")

    # Assert
    assert "Chess Club" in response.json()


def test_each_activity_has_required_fields(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    for name, details in response.json().items():
        assert required_fields.issubset(details.keys()), (
            f"Activity '{name}' is missing required fields"
        )
