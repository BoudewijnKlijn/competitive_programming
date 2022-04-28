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

        def get_best_contributor(
                role_skill_name,
                role_skill_level,
                contributor_names,
                contributor_skills,
                contributors_available_from,
                used_contributors,
        ):
            """
            Returns the best contributor for the given role

            Args:
                role_skill_name (str): Name of skill
                role_skill_level (int): Level of skill
                contributor_names (set): Set of names of contributors
                contributor_skills (dict): Dict of skills of contributors
                contributors_available_from (dict): Dict of contributors and their available from
            """
            best_score = None  # the higher the score the better
            best_contributor_name = None
            for contributor_name in contributor_names:
                if contributor_name in used_contributors:
                    continue
                contributor_score = sum([
                    -1 * contributors_available_from[contributor_name],
                    -1 * sum(contributor_skills[contributor_name].values()),
                ])

                if best_score is None or contributor_score > best_score:
                    best_score = contributor_score
                    best_contributor_name = contributor_name
            return best_contributor_name

        projects = input_data.projects
        projects = sorted(projects, key=lambda x: (x.score - x.best_before) / x.nr_of_days / len(x.roles), reverse=True)

        for project in projects:
            used_contributors = []
            valid_team = True
            for role in project.roles:
                # get all contributors with the required skill and level
                valid_contributor_names = set()
                # TODO: from -1 to also include the ones valid with a mentor
                for level in range(role.level, max_levels[role.name] + 1):
                    valid_contributor_names.update(skills[(role.name, level)])
                if not valid_contributor_names:
                    # No contributor found for this role.
                    valid_team = False
                    break

                # choose the contributor with the best heuristic
                best_contributor = get_best_contributor(
                    role.name,
                    role.level,
                    valid_contributor_names,
                    contributors_skills,
                    contributors_available_from,
                    used_contributors,
                )

                if best_contributor is not None:
                    used_contributors.append(best_contributor)
                else:
                    # No contributor found for this role.
                    valid_team = False
                    break

            if valid_team:
                # update the earliest available time for all contributors
                project_start_time = max(
                    [contributors_available_from[contributor_name] for contributor_name in used_contributors])
                for role, contributor_name in zip(project.roles, used_contributors):
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
                for contributor_name in used_contributors:
                    for contributor in contributors:
                        if contributor.name == contributor_name:
                            project.contributors.append(contributor)
                            break

        # Filter projects that have no contributors
        executed_projects = [project for project in projects if len(project.contributors) == len(project.roles)]

        return Solution(executed_projects)
