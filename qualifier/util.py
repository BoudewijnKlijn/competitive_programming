import os

from qualifier.output_data import OutputData


def save_output(output: OutputData, for_input_file, score, user_name):
    for_input = os.path.splitext(for_input_file)[0]
    this_path = os.path.abspath(os.path.dirname(__file__))
    file_name = f'{for_input}_{score:09}_{user_name}.out'

    output_dir = os.path.join(this_path, 'outputs')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    output.save(os.path.join(this_path, 'outputs', file_name))
