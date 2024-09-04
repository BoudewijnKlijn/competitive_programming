from typing import List


class Solution:
    def robotSim(self, commands: List[int], obstacles: List[List[int]]) -> int:
        return self.more_complex_numbers(commands, obstacles)

    def naive(self, commands: List[int], obstacles: List[List[int]]) -> int:
        obstacle_set = set(map(tuple, obstacles))
        x, y = 0, 0
        dx, dy = 0, 1
        ans = 0
        for command in commands:
            if command < 0:
                dx, dy = self.change_direction(dx, dy, command)
            else:
                # move forward command times. except if there is an obstacle
                for _ in range(command):
                    if (x + dx, y + dy) in obstacle_set:
                        break
                    x += dx
                    y += dy
                ans = max(ans, int(x**2 + y**2))

        return ans

    def change_direction(self, dx, dy, command):
        direction = complex(dx, dy)
        match command:
            case -1:
                direction *= complex(0, -1)
            case -2:
                direction *= complex(0, 1)
        return direction.real, direction.imag

    def more_complex_numbers(
        self, commands: List[int], obstacles: List[List[int]]
    ) -> int:
        obstacle_set = set(complex(x, y) for x, y in obstacles)
        position = complex(0, 0)
        direction = complex(0, 1)
        ans = 0
        for command in commands:
            if command == -1:
                direction *= complex(0, -1)
            elif command == -2:
                direction *= complex(0, 1)
            else:
                # move forward command times. except if there is an obstacle
                for _ in range(command):
                    if position + direction in obstacle_set:
                        break
                    position += direction
                ans = max(ans, int(position.real**2 + position.imag**2))
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["naive", "more_complex_numbers"],
        data_file="leetcode_0874_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
