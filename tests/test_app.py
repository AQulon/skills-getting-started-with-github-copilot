from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app, follow_redirects=False)


def test_root_redirects_to_static_index():
    # Arrange

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activity_details():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == 9
    assert activities["Chess Club"]["description"] == (
        "Learn strategies and compete in chess tournaments"
    )
    assert activities["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_student_to_activity():
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Soccer%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Soccer Club"
    }
    assert email in client.get("/activities").json()["Soccer Club"]["participants"]


def test_signup_rejects_duplicate_student():
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }


def test_signup_rejects_unknown_activity():
    # Arrange

    # Act
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_student_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_rejects_missing_participant():
    # Arrange

    # Act
    response = client.delete(
        "/activities/Soccer%20Club/participants/student%40mergington.edu"
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}


def test_unregister_rejects_unknown_activity():
    # Arrange

    # Act
    response = client.delete(
        "/activities/Unknown%20Club/participants/student%40mergington.edu"
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}