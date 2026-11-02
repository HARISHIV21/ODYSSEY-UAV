import math


class MissionValidationError(ValueError):
    """Raised when a mission configuration is invalid."""


class MissionValidator:
    """Validates mission configuration before flight execution."""

    REQUIRED_MISSION_FIELDS = (
        "mission_name",
        "takeoff_altitude",
        "waypoints",
    )

    REQUIRED_WAYPOINT_FIELDS = (
        "north",
        "east",
        "down",
    )

    @classmethod
    def validate(cls, mission):
        if not isinstance(mission, dict):
            raise MissionValidationError(
                "Mission must be a JSON object."
            )

        for field in cls.REQUIRED_MISSION_FIELDS:
            if field not in mission:
                raise MissionValidationError(
                    f"Missing mission field: {field}"
                )

        if not isinstance(mission["mission_name"], str):
            raise MissionValidationError(
                "mission_name must be a string."
            )

        if not mission["mission_name"].strip():
            raise MissionValidationError(
                "mission_name cannot be empty."
            )

        cls._validate_number(
            mission["takeoff_altitude"],
            "takeoff_altitude",
            minimum_exclusive=0,
        )

        waypoints = mission["waypoints"]

        if not isinstance(waypoints, list) or not waypoints:
            raise MissionValidationError(
                "Mission must contain at least one waypoint."
            )

        for index, waypoint in enumerate(waypoints):
            if not isinstance(waypoint, dict):
                raise MissionValidationError(
                    f"Waypoint {index + 1} must be an object."
                )

            for field in cls.REQUIRED_WAYPOINT_FIELDS:
                if field not in waypoint:
                    raise MissionValidationError(
                        f"Waypoint {index + 1} is missing '{field}'."
                    )

                cls._validate_number(
                    waypoint[field],
                    f"Waypoint {index + 1} {field}",
                )

            if "yaw" in waypoint:
                cls._validate_number(
                    waypoint["yaw"],
                    f"Waypoint {index + 1} yaw",
                )

        return True

    @staticmethod
    def _validate_number(value, field_name, minimum_exclusive=None):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise MissionValidationError(
                f"{field_name} must be a number."
            )

        if not math.isfinite(value):
            raise MissionValidationError(
                f"{field_name} must be finite."
            )

        if minimum_exclusive is not None and value <= minimum_exclusive:
            raise MissionValidationError(
                f"{field_name} must be greater than {minimum_exclusive}."
            )
