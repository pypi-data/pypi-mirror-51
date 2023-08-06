from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import (
        Set,
    )
    from ..models import (
        Trip,
        Route,
        Objective,
        OptimizationDirection,
    )


class Result(object):

    def __init__(self, fleet, job, algorithm_cls, planning, computation_time):
        self.fleet = fleet
        self.job = job
        self.algorithm_cls = algorithm_cls
        self.planning = planning
        self.computation_time = computation_time

    @property
    def trips(self) -> Set[Trip]:
        return self.job.trips

    @property
    def routes(self) -> Set[Route]:
        return self.planning.routes

    @property
    def completed_trips(self) -> Set[Trip]:
        trips: Set[Trip] = set()
        for route in self.routes:
            trips |= set(route.loaded_trips)
        return trips

    @property
    def coverage_rate(self):
        return len(self.completed_trips) / len(self.job.trips)

    @property
    def objective(self) -> Objective:
        return self.job.objective

    @property
    def optimization_function(self) -> float:
        return self.objective.optimization_function(self)

    @property
    def direction(self) -> OptimizationDirection:
        return self.objective.direction
