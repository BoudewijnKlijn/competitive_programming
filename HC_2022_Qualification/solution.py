from valcon import OutputData


class Solution(OutputData):
    def __init__(self, projects: list):
        self.projects = projects

    def save(self, filename: str):
        with open(filename, 'w') as file:
            file.write(str(len(self.projects)) + '\n')
            for project in self.projects:
                assert project.contributors, "submitted projets should be executed and thus have contributors"

                file.write(f'{project.name}\n')
                file.write(' '.join([c.name for c in project.contributors]) + '\n')

    def __repr__(self):
        return str(self.projects)
