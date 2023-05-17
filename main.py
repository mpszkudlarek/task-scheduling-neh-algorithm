import timeit

# read data from .DAT file and save it to list
file_input = [tuple(map(int, i.rstrip().split()))
              for i in open('data/NEH1.DAT').readlines()]
# count weight of each row and save it to dictionary
weights = {}
for i, row in enumerate(file_input[1:], start=0):
    weights[i] = sum(row)
# sort weights in descending order
sortedWeights = sorted(weights.items(), key=lambda x: x[1], reverse=True)


# function to calculate Cmax for given order of tasks
def get_cmax(order, lines):
    # create list of machines
    machine = [0] * lines[0][1]
    # iterate over tasks and machines
    for x in order:
        for y in range(lines[0][1]):
            if y == 0:
                machine[y] += lines[x + 1][y]
            else:
                if machine[y] >= machine[y - 1]:
                    machine[y] += lines[x + 1][y]
                else:
                    machine[y] = machine[y - 1] + lines[x + 1][y]
    # calculate total time taken
    cmax = machine[-1]
    return cmax


# function to find best order of tasks
def find_order(list_of_weights, lines):
    # initialize variables
    best_index = 0
    order = []
    current_best_time = float('inf')
    measurement_start = timeit.default_timer()
    # iterate over tasks
    for task in list_of_weights:
        # add task to all possible positions in order
        for i in range(len(order) + 1):
            order.insert(i, task[0])
            # calculate time for new order
            local_time = get_cmax(order, lines)
            # update best order if necessary
            if local_time < current_best_time:
                current_best_time = local_time
                best_index = i
            order.pop(i)
        # add task to best position in order
        order.insert(best_index, task[0])
        current_best_time = float('inf')
    measurement_finish = timeit.default_timer()

    # calculate and return final order and Cmax
    c_max = get_cmax(order, lines)

    print('Cmax:', c_max)
    print('Order:', [x + 1 for x in order])
    print('Execution time:', measurement_finish - measurement_start, 'seconds')


find_order(sortedWeights, file_input)
