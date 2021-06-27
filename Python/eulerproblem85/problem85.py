
def calculate_number_of_inner_rectangles(width, height):
    number_of_inner_rectangles = 0
    for inner_width in range(1, width+1):
        for inner_height in range(1, height+1):
            for x_pos in range(1, width - inner_width + 2):
                for y_pos in range(1, height - inner_height + 2):
                    number_of_inner_rectangles += 1
    return number_of_inner_rectangles


def main():
    max_size = 100
    goal = 2 * 10**6
    closest = None

    # Define large rectangle.
    for width in range(1, max_size+1):
        for height in range(1, width+1):

            # Calculate inner rectangles.
            number_of_inner_rectangles = calculate_number_of_inner_rectangles(width, height)

            # Verify if better than current best.
            difference = abs(goal - number_of_inner_rectangles)
            if closest is None or difference < closest:
                closest = difference
                closest_width = width
                closest_height = height
                print(f"{closest_width}x{closest_height} = {number_of_inner_rectangles}. Difference: {closest}")

                # 77x36 = 1999998. Difference: 2
                # area 77*36 = 2772


if __name__ == "__main__":
    main()
