from collections import defaultdict
from dataclasses import dataclass, field

from valcon import InputData


@dataclass
class Role:
    name: str
    level: int


class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = defaultdict(int)
        for skill in skills:
            self.skills[skill.name] = skill.level

    def get_level(self, role: Role):
        return self.skills[role.name]

    def __repr__(self):
        return f"Contributor(name: {self.name}, skills: {self.skills})"


@dataclass
class Project:
    name: str
    roles: [Role]
    nr_of_days: int
    score: int
    best_before: int

    contributors: [Contributor] = field(default_factory=list)

    def has_mentor(self, skill: Role) -> bool:
        role_level = skill.level

        return any(contributor.get_level(skill) >= role_level for contributor in self.contributors)


class ProblemData(InputData):
    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            meta_data, *raw_data = file.readlines()

        contributors, projects = [int(x) for x in meta_data.strip().split(' ')]

        self.contributors = []
        self.projects = []

        data_index = iter(range(len(raw_data)))
        for i in range(contributors):
            contributor_name, nr_of_skills = raw_data[next(data_index)].strip().split(' ')
            nr_of_skills = int(nr_of_skills)
            skills = []
            for j in range(nr_of_skills):
                role, level = raw_data[next(data_index)].strip().split()
                level = int(level)
                skills.append(Role(role, level))
            self.contributors.append(Contributor(contributor_name, skills))

        for i in range(projects):
            project_name, nr_of_days, score, best_before, nr_of_roles = raw_data[next(data_index)].strip().split(' ')
            nr_of_roles = int(nr_of_roles)
            nr_of_days = int(nr_of_days)
            roles = []
            for j in range(nr_of_roles):
                role, level = raw_data[next(data_index)].strip().split()
                level = int(level)
                roles.append(Role(role, level))
            self.projects.append(Project(project_name, roles, int(nr_of_days), int(score), int(best_before)))
