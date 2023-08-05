from random import uniform, randint
from typing import Set

import jinete as jit


def generate_one_surface(*args, **kwargs) -> jit.Surface:
    return jit.GeometricSurface(metric=jit.DistanceMetric.MANHATTAN, *args, **kwargs)


def generate_surfaces(n: int, *args, **kwargs) -> Set[jit.Surface]:
    return {
        generate_one_surface(*args, **kwargs) for _ in range(n)
    }


def generate_one_position(x_min: float = -100, x_max: float = 100, y_min: float = -100,
                          y_max: float = 100, surface: jit.Surface = None, *args, **kwargs) -> jit.Position:
    if surface is None:
        surface = generate_one_surface(*args, **kwargs)

    return surface.get_or_create_position([uniform(x_min, x_max), uniform(y_min, y_max)])


def generate_positions(n: int, surface: jit.Surface = None, *args, **kwargs) -> Set[jit.Position]:
    if surface is None:
        surface = generate_one_surface(*args, **kwargs)
    return {
        generate_one_position(surface=surface, *args, **kwargs) for _ in range(n)
    }


def generate_one_trip(identifier: str = None, earliest_min: float = 0, earliest_max: float = 86400,
                      timeout_min: float = 1800,
                      timeout_max: float = 7200, load_time_min: float = 300, load_time_max: float = 900,
                      capacity_min: int = 1, capacity_max: int = 3, *args, **kwargs) -> jit.Trip:
    if identifier is None:
        identifier = str()
    origin, destination = tuple(generate_positions(2, *args, **kwargs))
    earliest = uniform(earliest_min, earliest_max)
    timeout = uniform(timeout_min, timeout_max)
    capacity = randint(capacity_min, capacity_max)
    load_time = uniform(load_time_min, load_time_max)
    return jit.Trip(identifier, origin, destination, earliest, timeout, load_time, capacity)


def generate_trips(n: int, *args, **kwargs) -> Set[jit.Trip]:
    return {
        generate_one_trip(str(i), *args, **kwargs) for i in range(n)
    }


def generate_one_planned_trip(feasible: bool, route: jit.Route = None, *args, **kwargs) -> jit.PlannedTrip:
    trip = generate_one_trip(*args, **kwargs)

    # TODO: Improve feasible randomness.
    if feasible:
        down_time = 0
    else:
        down_time = jit.MAX_FLOAT

    initial = route.last_position

    if route is None:
        route_idx = None
    else:
        # route_idx = len(route.loaded_planned_trips)
        route_idx = route.loaded_planned_trips_count

    return jit.PlannedTrip(
        route=route,
        trip=trip,
        initial=initial,
        route_idx=route_idx,
        down_time=down_time,
    )


def generate_planned_trips(n: int, *args, **kwargs) -> Set[jit.PlannedTrip]:
    return {
        generate_one_planned_trip(*args, **kwargs) for _ in range(n)
    }


def generate_one_vehicle(capacity_min: int = 1, capacity_max: int = 3, earliest_min: float = 0,
                         earliest_max: float = 86400, timeout_min: float = 14400, timeout_max: float = 28800,
                         idx: int = 0, *args, **kwargs) -> jit.Vehicle:
    # TODO: Increase parameter options.
    capacity = randint(capacity_min, capacity_max)
    initial = generate_one_position(*args, **kwargs)
    earliest = uniform(earliest_min, earliest_max)
    timeout = uniform(timeout_min, timeout_max)
    return jit.Vehicle(str(idx), initial, capacity=capacity, earliest=earliest, timeout=timeout)


def generate_vehicles(n: int, *args, **kwargs) -> Set[jit.Vehicle]:
    return {
        generate_one_vehicle(idx=idx, *args, **kwargs) for idx in range(n)
    }


def generate_one_route(feasible: bool, planned_trips_min: int = 1, planned_trips_max: int = 20,
                       surface: jit.Surface = None, *args, **kwargs) -> jit.Route:
    if surface is None:
        surface = generate_one_surface(*args, **kwargs)
    vehicle = generate_one_vehicle(surface=surface, *args, **kwargs)
    route = jit.Route(vehicle)

    planned_trips_len = randint(planned_trips_min, planned_trips_max)
    cut_len = vehicle.timeout / planned_trips_len

    planned_trip = generate_one_planned_trip(
        feasible=feasible,
        route=route,
        earliest_min=vehicle.earliest,
        earliest_max=vehicle.earliest,
        timeout_min=cut_len,
        timeout_max=cut_len,
        surface=surface,
    )

    route.append_planned_trip(planned_trip)

    for i in range(planned_trips_len):
        planned_trip = generate_one_planned_trip(
            feasible=feasible,
            route=route,
            earliest_min=route.last_time,
            earliest_max=route.last_time,
            timeout_min=cut_len,
            timeout_max=cut_len,
            surface=surface,
        )

        route.append_planned_trip(planned_trip)
    route.finish()
    vehicle.timeout = route.last_time - vehicle.earliest
    return route


def generate_routes(n: int, *args, **kwargs) -> Set[jit.Route]:
    return {
        generate_one_route(*args, **kwargs) for _ in range(n)
    }
