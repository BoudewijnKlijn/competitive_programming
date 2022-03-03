import random

from .base_strategy import BaseStrategy
from ..problem_data import ProblemData
from ..solution import Solution
from collections import defaultdict


class BaselineStrategy(BaseStrategy):
    def __init__(self, seed: int = None):
        """
        Initializes a BaseLineStrategy which simply assigns every contributor to a project based on first come (in list)
        first served (only if it has the required skill)

        Args:
            seed (int): Seed for random generator
        """
        if seed:
            self.seed = seed
        else:
            self.seed = random.randint(0, 999_999_999)
        super().__init__(self.seed)

    def solve(self, input_data: ProblemData) -> Solution:
        contributors = input_data.contributors
        contributors_skills = input_data.contributors_dict
        contributors_available_from = {contributor.name: 0 for contributor in contributors}

        unique_skills = {skill for contributor in contributors for skill in contributor.skills}

        # make dict with skills and level to prevent looping over all contributors
        # key=tuple(skill, level), value=set of contributors with skill and level
        max_levels = defaultdict(int)
        skills = defaultdict(set)
        for skill_name in unique_skills:
            for contributor in contributors:
                if skill_name in contributor.skills:
                    skills[(skill_name, contributor.skills[skill_name])].add(contributor.name)
                    if contributor.skills[skill_name] > max_levels[skill_name]:
                        max_levels[skill_name] = contributor.skills[skill_name]
                else:
                    skills[(skill_name, 0)].add(contributor.name)
        # print('skills', skills)
        # print(max_levels)
        # exit()

        projects = input_data.projects
        projects = sorted(projects, key=lambda x: (x.score - x.best_before) / x.nr_of_days / len(x.roles), reverse=True)

        for project in projects:
            earliest_contributors = []
            valid_team = True
            for role in project.roles:
                # Assign the contributor that has the required skill and is first available
                earliest_valid_contributor = None

                # get all contributors with the required skill and level
                valid_contributor_names = set()
                # TODO: from -1 to also include the ones valid with a mentor
                for level in range(role.level, max_levels[role.name] + 1):
                    valid_contributor_names.update(skills[(role.name, level)])

                # choose the first one that is available
                for contributor_name in valid_contributor_names:
                    if contributor_name in earliest_contributors:
                        # Contributor can only have 1 role
                        continue
                    if earliest_valid_contributor is None or \
                            contributors_available_from[contributor_name] < \
                            contributors_available_from[earliest_valid_contributor]:
                        earliest_valid_contributor = contributor_name

                if earliest_valid_contributor is not None:
                    earliest_contributors.append(earliest_valid_contributor)
                else:
                    # No contributor found for this role.
                    valid_team = False

            if valid_team:
                # update the earliest available time for all contributors
                project_start_time = max(
                    [contributors_available_from[contributor_name] for contributor_name in earliest_contributors])
                for role, contributor_name in zip(project.roles, earliest_contributors):
                    contributors_available_from[contributor_name] = project_start_time + project.nr_of_days

                    # update skills of contributors
                    # increase level of skill if contributor level was equal or lower than required level
                    old_level = contributors_skills[contributor_name].get(role.name, 0)
                    if role.level <= old_level:
                        new_level = old_level + 1
                        contributors_skills[contributor_name].update({role.name: new_level})
                        skills[(role.name, old_level)].remove(contributor_name)  # remove from old skill level
                        skills[(role.name, new_level)].add(contributor_name)  # add to new skill level

                        # update max level
                        if new_level > max_levels[role.name]:
                            max_levels[role.name] = new_level

                # convert contributor new to complete contributor object
                for contributor_name in earliest_contributors:
                    for contributor in contributors:
                        if contributor.name == contributor_name:
                            project.contributors.append(contributor)
                            break

        # Filter projects that have no contributors
        executed_projects = [project for project in projects if len(project.contributors) == len(project.roles)]

        return Solution(executed_projects)
