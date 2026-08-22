from math import asin, cos, radians, sin, sqrt


class DistanceService:
    @staticmethod
    def calculate_distance(origin_latitude: float, origin_longitude: float, destination_latitude: float, destination_longitude: float) -> float:
        earth_radius_km = 6371.0088
        latitude_delta = radians(destination_latitude - origin_latitude)
        longitude_delta = radians(destination_longitude - origin_longitude)
        value = sin(latitude_delta / 2) ** 2 + cos(radians(origin_latitude)) * cos(radians(destination_latitude)) * sin(longitude_delta / 2) ** 2
        return earth_radius_km * 2 * asin(sqrt(value))