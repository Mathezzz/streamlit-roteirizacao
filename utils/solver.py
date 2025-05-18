# -*- coding: utf-8 -*-
"""
Created on Sun May 18 10:42:16 2025

@author: ander
"""

from ortools.constraint_solver import routing_enums_pb2, pywrapcp

def solve_tsp(matrix: list[list[int]]) -> list[int]:
    n = len(matrix)
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def dist_cb(i, j):
        return matrix[manager.IndexToNode(i)][manager.IndexToNode(j)]

    idx = routing.RegisterTransitCallback(dist_cb)
    routing.SetArcCostEvaluatorOfAllVehicles(idx)

    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    sol = routing.SolveWithParameters(params)

    route = []
    i = routing.Start(0)
    while not routing.IsEnd(i):
        route.append(manager.IndexToNode(i))
        i = sol.Value(routing.NextVar(i))
    route.append(manager.IndexToNode(i))
    return route
