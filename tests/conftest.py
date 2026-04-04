"""Shared test fixtures for gtable_py."""

import pytest
from grid_py import Unit, circle_grob, lines_grob, polygon_grob, rect_grob


@pytest.fixture
def grob1():
    return rect_grob()


@pytest.fixture
def grob2():
    return circle_grob()


@pytest.fixture
def grob3():
    return lines_grob()


@pytest.fixture
def grob4():
    return polygon_grob()


@pytest.fixture
def cm():
    return Unit(1, "cm")


@pytest.fixture
def cm2():
    return Unit(2, "cm")


@pytest.fixture
def cm5():
    return Unit(5, "cm")


@pytest.fixture
def null():
    return Unit(1, "null")
