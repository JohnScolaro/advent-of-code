import bisect

def find_numbers_that_sum_to_goal(input_file: str, n: int, goal: int):
    """Find n numbers that sum to create another number from an input file
    
    Args:
        input_file (str): File to get numbers from.
        n (int): Number of numbers to sum together.
        goal: Value of the summation we are trying to find numbers to.

    Returns:
        None
    """

    if (n <= 0):
        print('n must be greater than 0.')
        return

    # Create a sorted list from the input files
    sorted_list = []
    with open('input.txt', 'r') as fp:
        for line in fp:
            bisect.insort_left(sorted_list, int(line))

    # Recursively select numbers from the sorted list and test to see if they sum to make x. 
    numbers_selected = []

    if select_new_number(sorted_list, numbers_selected, n, goal):
        print_output(numbers_selected)
    else:
        print("No valid combinations.")
    return

def select_new_number(sorted_list: list, numbers_selected: list, n: int, goal: int):
    """
    If n is 5, we are selecting 5 numbers to sum together to equal something.
    This function is called once for each number, and it iterates through all the
    possible numbers that it could be.
    """

    for i in range(len(sorted_list)):
        # Pop number out of the sorted list and put it into our selection array
        selected_number = sorted_list.pop(i)
        numbers_selected.append(selected_number)

        # If this is the last number, check all the numbers to see if they sum to the goal
        if (len(numbers_selected) == n):
            if (sum(numbers_selected) == goal):
                # If they do, return true
                return True
            else:
                # If they don't return it to the sorted list, and try another number
                numbers_selected.pop()
                bisect.insort_left(sorted_list, selected_number)
        else:
            # If we aren't at the last number, run this function again to iterate over a list of acceptable numbers
            max_number_to_consider_looking_at = goal - sum(numbers_selected)
            index_of_max_number = bisect.bisect_right(sorted_list, max_number_to_consider_looking_at)
            if select_new_number(sorted_list[0:index_of_max_number], numbers_selected, n, goal):
                return True
            else:
                # If we get here, then none of the combinations work with this number, so put it back into the list and continue
                numbers_selected.pop()
                bisect.insort_left(sorted_list, selected_number)

    return False

def print_output(output_array: list):
    """Prints the output in readable form."""

    str_output_array = [str(x) for x in output_array]

    # Print sum
    string_to_print = ' + '.join(str_output_array)
    string_to_print += ' = ' + str(sum(output_array))
    print(string_to_print)

    # Print multiplication
    product = 1
    for x in output_array:
        product *= x
    string_to_print = ' * '.join(str_output_array)
    string_to_print += ' = ' + str(product)
    print(string_to_print)


if __name__ == "__main__":
    find_numbers_that_sum_to_goal("input.txt", 2, 2020)
    find_numbers_that_sum_to_goal("input.txt", 3, 2020)
    # There exist combinations for 4 and 5 numbers, but none more that I could find.    