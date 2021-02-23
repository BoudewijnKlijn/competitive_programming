from qualifier.output_data import OutputData


def validate_output(output: OutputData) -> bool:
    return True


def calculate_score(solution: OutputData) -> int:
    if not validate_output(solution):
        raise ValueError('Not valid output')

    return 0
