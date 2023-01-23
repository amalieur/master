from haversine import haversine, Unit

# Helper function to compute distance between a list of coordinates (Trajectory distance)
# Haversine distance used

def calculate_trajectory_distance(positions: list[tuple[float]]) -> float:
    """
    Calculate the trajectory distance for a trajectory

    :param: List of coordinates (lat, lon)
    
    :return: Float -> Combined distance between all pairs of points
    """
    distance = 0
    for i in range(1, len(positions)):
        from_location = positions[i-1]
        to_location = positions[i]

        distance += haversine(from_location, to_location, unit=Unit.KILOMETERS)
    return distance
