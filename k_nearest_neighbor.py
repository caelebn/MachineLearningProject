import math

#  calculate_distance_list(int tuple_size, tuples [])
#  INPUTS: int tuple_size- the size of each of the tuples
#          tuples[]- a list of all tuples that contain data points.
#  OUTPUTS: distances[tuple[t1, t2, d]] - a list of tuples that contain tuple 1, tuple 2, and the distance between them.
#  INFO: calculate_distance_list(...) goes through 0 to n tuples and calculates the distance between the points
#           contained.
#           It does this by calculating all distances between tuples 0 and 1, 0 and 2, ..., 0 and n-1, 1 and 2,
#           ..., 1 and n, ..., n-1, n. It saves each of these couple of points and their correlating distance into a
#           tuple, which is then stored into a list. This list of tuples is returned as the output.
#  FUNCTION STATUS: COMPLETE (NEEDS TESTING)


def calculate_distance_list(tuples):
    distances = []
    for i in range(0, len(tuples)-1):
        for j in range(i+1, len(tuples)):
            dist = calculate_2way_distance(tuples[i], tuples[j])
            t_to_add = (tuples[i], tuples[j], dist)
            distances.append(t_to_add)
    return distances


#  calculate_2way_distance(t1, t2)
#  INPUTS: tuple t1- a tuple of data points
#          tuple t2- a tuple of data points
#  OUTPUTS: Euclidean distance between t1 and t2
#  INFO: Calculates the euclidean distance between tuple t1 and tuple t2. Returns the final distance.
#        sqrt((x2-x1)^2 + (y2-y1)^2 + ... + (n2-n1)^2)
#  FUNCTION STATUS: WORKING AS INTENDED


def calculate_2way_distance(t1, t2):
    sum_total = 0
    for index in range(0, len(t1)):
        difference = t1[index] - t2[index]
        two_point_diffsq = difference * difference
        sum_total += two_point_diffsq
    return math.sqrt(sum_total)

#  TEST HERE


def main():
    t1 = (5, 10)
    t2 = (10, 15)
    distance = calculate_2way_distance(t1, t2)
    print('distance', distance)
    distances = calculate_distance_list([t1, t2])
    print('distance tuples', distances)


main()
