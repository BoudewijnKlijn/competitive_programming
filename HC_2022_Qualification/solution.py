from valcon import OutputData


class Solution(OutputData):
    def __init__(self, projects: list):
        self.projects = projects

    def save(self, filename: str):
        with open(filename, 'w') as file:
            file.write(str(len(self.projects)) + '\n')
            for project in self.projects:
                file.write(f'{project.name} {len(project.contributors)}')
                file.write(' '.join(project.contributors) + '\n')
                