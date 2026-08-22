from __future__ import annotations


class RadiusExpansionService:
    def levels(self, initial: float, maximum: float) -> list[float]:
        configured = [initial, 25, 50, 100, maximum]
        return sorted({round(min(maximum, value), 2) for value in configured if value >= initial})