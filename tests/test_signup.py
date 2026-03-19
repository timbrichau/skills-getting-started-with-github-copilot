def test_signup_for_valid_activity_returns_200(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200


def test_signup_adds_student_to_participants(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_returns_confirmation_message(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert "message" in response.json()
    assert email in response.json()["message"]


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    activity = "Underwater Basket Weaving"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404


def test_signup_duplicate_student_returns_400(client):
    # Arrange — michael is already seeded into Chess Club
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400


def test_unregister_from_valid_activity_returns_200(client):
    # Arrange — michael is seeded into Chess Club
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200


def test_unregister_removes_student_from_participants(client):
    # Arrange — michael is seeded into Chess Club
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_returns_confirmation_message(client):
    # Arrange — michael is seeded into Chess Club
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert "message" in response.json()
    assert email in response.json()["message"]


def test_unregister_from_unknown_activity_returns_404(client):
    # Arrange
    activity = "Underwater Basket Weaving"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404


def test_unregister_student_not_signed_up_returns_404(client):
    # Arrange — this email is not enrolled in Chess Club
    activity = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404


def test_signup_then_unregister_round_trip(client):
    # Arrange — fresh email not in any activity
    activity = "Chess Club"
    email = "roundtrip@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    unregister_response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
