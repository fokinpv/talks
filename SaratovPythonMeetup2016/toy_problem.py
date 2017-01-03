import itertools
from collections import namedtuple

import pulp
import sympy
from prettytable import PrettyTable

(Revenue, CostPerKg, Weight, ItemPenalty, Penalty, InTime) = sympy.symbols([
    'Revenue', 'CostPerKg', 'Weight', 'ItemPenalty', 'Penalty', 'InTime'
])

ItemCost = Revenue - CostPerKg * Weight  # - Penalty

Penalty = sympy.Piecewise(
    (ItemPenalty, sympy.Not(InTime)),
    (0, InTime)
)

print(Penalty)

Box = namedtuple('Box', ['revenue', 'weight', 'required'])
Truck = namedtuple('Truck', ['capacity', 'cost_per_kg'])

trucks = {
    'truck1': Truck(capacity=2.0, cost_per_kg=1.5),
    'truck2': Truck(capacity=10.0, cost_per_kg=0.9),
}

boxes = {
    'box1': Box(revenue=5.0, weight=1.0, required=True),
    'box1.1': Box(revenue=60.0, weight=5.0, required=True),
    'box1.2': Box(revenue=15.0, weight=2.5, required=False),
    'box2': Box(revenue=11.0, weight=1.5, required=False),
    'box3': Box(revenue=15.0, weight=2.5, required=False),
}

possible_assignments = list(itertools.product(boxes, trucks))

b2t_costs = {}
for box, truck in possible_assignments:
    item_cost = ItemCost.subs({
        'Revenue': boxes[box].revenue,
        'CostPerKg': trucks[truck].cost_per_kg,
        'Weight': boxes[box].weight
    })
    print(box, truck, item_cost)
    b2t_costs[box, truck] = item_cost

x = {
    (b, t): pulp.LpVariable('b2t_%s_%s' % (b, t), cat=pulp.LpBinary)
    for b, t in possible_assignments
}

truck_usage = {
    t: pulp.LpVariable(
        'truck_usage_%s' % t, lowBound=0, upBound=50, cat=pulp.LpContinuous
    )
    for t in trucks
}

truck_free = {
    t: pulp.LpVariable(
        'truck_free_%s' % t, lowBound=0, upBound=50, cat=pulp.LpContinuous
    )
    for t in trucks
}

optimization_model = pulp.LpProblem(
    'Boxes to Trucks Assignment Model', pulp.LpMaximize
)

optimization_model += sum([
    x[box_to_truck] * b2t_costs[box_to_truck]
    for box_to_truck in possible_assignments
])

optimization_model.objective += sum([
    #  truck_free[truck]
    -1 * truck_free[truck] * (trucks[truck].cost_per_kg / 2)
    for truck in truck_free
])

for truck in trucks:
    optimization_model += sum([
        boxes[box_to_truck[0]].weight * x[box_to_truck]
        for box_to_truck in possible_assignments
        if truck in box_to_truck
    ]) <= trucks[truck].capacity

for truck in trucks:
    optimization_model += sum([
        boxes[box_to_truck[0]].weight * x[box_to_truck]
        for box_to_truck in possible_assignments
        if truck in box_to_truck
    ]) == truck_usage[truck]

for truck in trucks:
    optimization_model += sum([
        boxes[box_to_truck[0]].weight * x[box_to_truck]
        for box_to_truck in possible_assignments
        if truck in box_to_truck
    ]) + truck_free[truck] == trucks[truck].capacity

for box in boxes:
    if boxes[box].required:
        optimization_model += sum([
            x[box_to_truck]
            for box_to_truck in possible_assignments
            if box in box_to_truck
        ]) == 1
    else:
        optimization_model += sum([
            x[box_to_truck]
            for box_to_truck in possible_assignments
            if box in box_to_truck
        ]) <= 1


optimization_model.writeLP('optimization_model.lp')


solver = pulp.PULP_CBC_CMD(msg=1)
status = optimization_model.solve(solver)

print(pulp.LpStatus[status])

prettytable = PrettyTable(['Truck', 'Capacity', 'Used', 'Free', 'Boxes'])

for truck in trucks:
    row = []
    row.append(truck)
    row.append(trucks[truck].capacity)
    row.append(truck_usage[truck].value())
    row.append(truck_free[truck].value())
    _row_boxes = []
    for box in boxes:
        if x[box, truck].value() != 1.0:
            continue

        _row_boxes.append('%s(%s)' % (box, boxes[box].weight))
    row.append(', '.join(_row_boxes))
    prettytable.add_row(row)


print(prettytable)
