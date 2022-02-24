from dataclasses import dataclass

from valcon import InputData


@dataclass
class Role:
    name: str
    level: int


@dataclass
class Contributor:
    name: str
    skills: [Role]


@dataclass
class Project:
    name: str
    roles: [Role]


class ProblemData(InputData):
    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            meta_data, *raw_data = file.readlines()

        contributors, projects = [int(x) for x in meta_data.strip().split(' ')]

        self.contributors = []
        self.projects = []

        for i in range(contributors):
            contributor_name, nr_of_skills = raw_data.pop(0).strip().split(' ')
            nr_of_skills = int(nr_of_skills)
            skills = []
            for j in range(nr_of_skills):
                role, level = raw_data.pop(0).strip().split()
                level = int(level)
                skills.append(Role(role, level))
            self.contributors.append(Contributor(contributor_name, skills))

        for i in range(projects):
            project_name, nr_of_days, score, best_before, nr_of_roles = raw_data.pop(0).strip().split(' ')
            nr_of_roles = int(nr_of_roles)
            roles = []
            for j in range(nr_of_roles):
                role, level = raw_data.pop(0).strip().split()
                level = int(level)
                roles.append(Role(role, level))
            self.projects.append(Project(project_name, roles))
