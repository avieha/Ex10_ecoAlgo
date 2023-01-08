import doctest
import statistics
from typing import List


def bin_search(C, citizen_votes):
    # print("citizen votes:", citizen_votes)
    start = 0
    end = 1
    while end > start:
        functions = []
        merged = []
        t = (start + end) / 2
        for i in range(1, len(citizen_votes)):  # creating linear functions as we learned
            functions.append(C * min(1, i * t))
        # print("\nt:", t, "linear functions:", functions)
        for i in range(len(citizen_votes[0])):  # iterating each topic, merging with functions
            vec = []
            for citizen in citizen_votes:
                vec.append(citizen[i])
            vec += functions
            vec.sort()
            merged.append(vec)
        medians_list = [statistics.median(vec) for vec in merged]
        # print("medians list:",medians_list)
        medians_sum = sum(medians_list)
        if medians_sum < C:
            start = t
        if medians_sum > C:
            end = t
        if medians_sum == C:
            # print("the right t is:", t)
            return medians_list


def compute_budget(total_budget: float, citizen_votes: List[List]) -> List[float]:
    """
    :param total_budget:
    :param citizen_votes:
    :return: list of medians for each topic
    >>> # the right t is: 0.5
    >>> citizen_votes = [[100, 0, 0], [0, 0, 100]]
    >>> compute_budget(100, citizen_votes)
    [50.0, 0, 50.0]
    >>> # the right t is: 0.06666666666666667
    >>> citizen_votes = [[6,6,6,6,0,0,6,0,0],[0,0,6,6,6,6,0,6,0],[6,6,0,0,6,6,0,0,6]]
    >>> compute_budget(30, citizen_votes)
    [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 2.0, 2.0]
    >>> # the right t is: 0.25
    >>> citizen_votes = [[100, 30, 0], [15, 100, 15],[50, 50, 30]]
    >>> compute_budget(130, citizen_votes)
    [50, 50, 30]
    """
    result = bin_search(total_budget, citizen_votes)
    return result


def fair_groups(total_budget: float, citizen_votes: List[List]):
    """
    :param total_budget:
    :param citizen_votes:
    >>> citizen_votes = [[100, 0, 0], [0, 0, 100]]
    >>> fair_groups(100,citizen_votes)
    computed budget: [50.0, 0, 50.0]
    given part: 0.5 , Kj/n: 0.5
    given part: 0.5 , Kj/n: 0.5
    budget is FAIR for groups
    >>> citizen_votes = [[30, 0, 0], [30, 0, 0], [0, 30, 0], [0, 30, 0], [30, 0, 0], [0, 0, 30], [0, 30, 0], [0, 30, 0],[0, 0, 30], [0, 0, 30]]
    >>> fair_groups(30, citizen_votes)
    computed budget: [9.000000000000002, 12.0, 9.000000000000002]
    given part: 0.30000000000000004 , Kj/n: 0.3
    given part: 0.4 , Kj/n: 0.4
    given part: 0.30000000000000004 , Kj/n: 0.3
    budget is FAIR for groups
    >>> citizen_votes = [[50,0,0,0,0,0,0,0,0],[0,0,0,0,50,0,0,0,0],[0,0,0,0,0,0,0,0,50]]
    >>> fair_groups(50,citizen_votes)
    computed budget: [16.666666666666668, 0, 0, 0, 16.666666666666668, 0, 0, 0, 16.666666666666668]
    given part: 0.33333333333333337 , Kj/n: 0.3333333333333333
    given part: 0.33333333333333337 , Kj/n: 0.3333333333333333
    given part: 0.33333333333333337 , Kj/n: 0.3333333333333333
    budget is FAIR for groups
    >>> citizen_votes = [[200, 0, 0], [0, 200, 0],[0, 0, 200]]
    >>> fair_groups(200,citizen_votes)
    computed budget: [66.66666666666667, 66.66666666666667, 66.66666666666667]
    given part: 0.33333333333333337 , Kj/n: 0.3333333333333333
    given part: 0.33333333333333337 , Kj/n: 0.3333333333333333
    given part: 0.33333333333333337 , Kj/n: 0.3333333333333333
    budget is FAIR for groups
    """
    result = compute_budget(total_budget, citizen_votes)
    print("computed budget:", result)
    num_of_supp = {}
    n = len(citizen_votes)
    for citizen in citizen_votes:
        for index, supp in enumerate(citizen):
            if citizen[index] == total_budget:
                v = num_of_supp.get(index)
                if not v:
                    num_of_supp[index] = 0
                num_of_supp[index] += 1
    # print("num of supp", num_of_supp)
    for index, part in enumerate(result):
        v = num_of_supp.get(index)
        if v:
            print("given part:", part / total_budget, ", Kj/n:", num_of_supp[index] / n)
            if part / total_budget < (num_of_supp[index] / n):
                print("budget is Not fair for groups")
                return
    print("budget is FAIR for groups")
    return


if __name__ == '__main__':
    failures, tests = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
