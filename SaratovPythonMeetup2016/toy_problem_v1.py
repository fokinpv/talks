import itertools
from collections import namedtuple

import pulp
import sympy
from prettytable import PrettyTable

CostPerKg, Weight = sympy.symbols([ 'CostPerKg', 'Weight' ])

ItemCost = CostPerKg * Weight

Box = namedtuple('Box', ['weight'])
Service = namedtuple('Service', ['capacity', 'cost_per_kg'])

services = {
    'service1': Service(capacity=2.0, cost_per_kg=1.5),
    'service2': Service(capacity=10.0, cost_per_kg=0.9),
}

boxes = {
    'box1': Box(weight=1.0),
    'box2': Box(weight=1.5),
    'box3': Box(weight=2.5),
    'box4': Box(weight=6.5),
}

possible_assignments = list(itertools.product(boxes, services))

b2s_costs = {}
for box, service in possible_assignments:
    item_cost = ItemCost.subs({
        'CostPerKg': services[service].cost_per_kg,
        'Weight': boxes[box].weight
    })
    b2s_costs[box, service] = item_cost


x = {
    (b, t): pulp.LpVariable('b2s_%s_%s' % (b, t), cat=pulp.LpBinary)
    for b, t in possible_assignments
}

model = pulp.LpProblem(
    'Assignment Model', pulp.LpMinimize
)

model += sum([
    x[box_to_service] * b2s_costs[box_to_service]
    for box_to_service in possible_assignments
])

for service in services:
    model += sum([
        boxes[box_to_service[0]].weight * x[box_to_service]
        for box_to_service in possible_assignments
        if service in box_to_service
    ]) <= services[service].capacity

for box in boxes:
    model += sum([
        x[box_to_service]
        for box_to_service in possible_assignments
        if box in box_to_service
    ]) == 1


model.writeLP('model.lp')

solver = pulp.PULP_CBC_CMD(msg=1)
status = model.solve(solver)

print(pulp.LpStatus[status])

prettytable = PrettyTable(['Service', 'Capacity', 'Boxes'])

for service in services:
    row = []
    row.append(service)
    row.append(services[service].capacity)
    _row_boxes = []
    for box in boxes:
        if x[box, service].value() != 1.0:
            continue

        _row_boxes.append('%s(%s)' % (box, boxes[box].weight))
    row.append(', '.join(_row_boxes))
    prettytable.add_row(row)


print(prettytable)
