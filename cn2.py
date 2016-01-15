#!/usr/bin/env python3

import math


LESS_THAN = 1
GREATER_THAN = 2
EQUAL_TO = 3


class Condition:
    def __init__(self, argument, condition, value):
        self.argument = argument
        self.condition = condition
        self.value = value

    def test(self, data):
        if self.argument not in data:
            return False

        d = data[self.argument]
        if self.condition == LESS_THAN:
            return d < self.value
        elif self.condition == GREATER_THAN:
            return d > self.value
        else:
            return d == self.value

    def __repr__(self):
        x = ["", "<", ">", "=="]
        return self.argument + " " + x[self.condition] + " " + str(self.value)


# Evaluate a complex for given data
# Note: complex is a set of conditions and represent their conjunction
#       each data contains value for all arguments and class
def evaluate(complex, data):
    # Use entropy to statistaclly evaluate the complex

    # Get data which statisfy all conditions of the complex
    # and get number of data belonging to each class
    classes = {}
    data1 = list()
    for d in data:
        satisfy = True
        for c in complex:
            if not c.test(d):
                satisfy = False

        if satisfy:
            data1.append(d)
            if d["class"] in classes:
                classes[d["class"]] += 1
            else:
                classes[d["class"]] = 1

    if len(data1) == 0:
        return -10000, None, []

    # Find probability for each class and get total entropy
    entropy = 0
    # Also calculate the most occuring class for this complex
    m = 0
    mclass = None

    for c in classes:
        if classes[c] > m:
            m = classes[c]
            mclass = c

        p = classes[c] / float(len(data1))
        entropy -= p * math.log2(p)

    # Return negative of entropy implying: more ordered
    # a data, better the classification
    return -entropy, mclass, data1


# Join a complex and a condition to new complex
def join(complex, condition):
    new = list()
    for c in complex:
        new.append(c)

    new.append(condition)
    return list(set(new))


# Compare if two complex are same:
def compare(c1, c2):
    for x in c1:
        if x not in c2:
            return False

    return True


# Find best complex for a given data
# Selectors is a set of all basic conditions
# max_size is the maximum number of conditions to hold in a complex
def find_best_complex(selectors, data):
    star = [list()]    # list of complexes, initialized with empty complex
    best = None
    evaluation = None
    cls = None
    dt = None

    condition = True
    while condition:
        newstar = list()
        for x in star:
            for y in selectors:
                newstar.append(join(x, y))

        useless = list()
        for x in newstar:
            for y in star:
                if compare(x, y):
                    useless.append(x)

        for a in useless:
            if a in newstar:
                newstar.remove(a)

        for c in newstar:
            e1, c1, d1 = evaluate(c, data)
            if not best or evaluation < e1:
                evaluation, cls, dt = e1, c1, d1
                best = c

        while len(newstar) > 3:
            worst, we = None, 0
            for c in newstar:
                e1, c1, d1 = evaluate(c, data)
                if not worst or we > e1:
                    worst, we = c, e1
            newstar.remove(worst)

        star = newstar
        condition = len(star) > 0

    return best, cls, dt


def cn2(data, selectors):
    # Make a copy of the data
    e = list()
    for d in data:
        e.append(d)

    # Rule is a set of tuple (complex, class) which means:
    # if complex then class
    rules = list()
    condition = True
    while condition:
        best, cls, covered = find_best_complex(selectors, e)

        for d in covered:
            e.remove(d)

        rules.append((best, cls))

        condition = (best is not None and len(e) > 0)

    return rules


# Creating training data
data = [
    {"class": "healthy",   "age": 5,  "height": 3,  "weight": 20},
    {"class": "healthy",   "age": 10, "height": 5,  "weight": 30},
    {"class": "healthy",   "age": 20, "height": 5,  "weight": 50},
    {"class": "healthy",   "age": 5,  "height": 4,  "weight": 25},
    {"class": "healthy",   "age": 10, "height": 4,  "weight": 28},
    {"class": "healthy",   "age": 20, "height": 6,  "weight": 60},

    {"class": "unhealthy",   "age": 5,  "height": 3,  "weight": 10},
    {"class": "unhealthy",   "age": 10, "height": 5,  "weight": 40},
    {"class": "unhealthy",   "age": 20, "height": 5,  "weight": 70},
    {"class": "unhealthy",   "age": 5,  "height": 4,  "weight": 15},
    {"class": "unhealthy",   "age": 10, "height": 4,  "weight": 18},
    {"class": "unhealthy",   "age": 20, "height": 6,  "weight": 30},
]

# Selectors containing basic conditions to create rules
selectors = [
    Condition("age", LESS_THAN, 15),
    Condition("age", GREATER_THAN, 15),
    Condition("height", LESS_THAN, 4.5),
    Condition("height", GREATER_THAN, 4.5),
    Condition("weight", LESS_THAN, 35),
    Condition("weight", GREATER_THAN, 35),
]


print(cn2(data, selectors))
