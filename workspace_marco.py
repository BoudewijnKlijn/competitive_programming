import valcon
import HC_2019_Qualification

if __name__ == '__main__':
    input_data = InputData(os.path.join(directory, file_name))

    my_strategy = StartFirstGreen(seed=random.randint(0, 1_000_000))
    # my_strategy = RandomStrategy(StartFirstGreen, seed=random.randint(0, 1_000_000), tries=10)
    # my_strategy = setup_evolution_strategy(file_name)

    print(f'Solving with strategy {my_strategy.name}...')
    output = my_strategy.solve(input_data)

    print(f'Running solution trough simulator...')
    score, _ = SimulatorV4(input_data, verbose=0).run(output)