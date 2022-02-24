from HC_2022_Qualification.problem_data import ProblemData
from HC_2022_Qualification.solution import Solution
from valcon.scorer import Scorer
from collections import defaultdict


class Score(Scorer):
    def __init__(self, input_data: ProblemData, verbose: bool = False):
        # self.project_index = {project.name: index for index, project in enumerate(input_data.projects)}
        self.verbose = verbose
        self.projects = input_data.projects
        self.contributors_available_from = {contributor.name: 0 for contributor in input_data.contributors}
        self.contributors = {contributor.name: contributor.skills for contributor in input_data.contributors}
        # for contributor in input_data.contributors:
        #     for role in contributor.skills:
        #         self.contributors[contributor.name][role.name] = role.level

    def calculate(self, output_data: Solution) -> int:
        score = 0

        # projects are completed in order of outputdata
        # first check if contributors have the required skill. they may be mentored
        # also check if contributors are available for the project (and not still busy on another project)
        # if they have the skill and are available, they are busy for the duration of the project.
        # at the end they might level up a skill (if they required skill was equal or higher than their skill (can at
        # most be 1 higher)
        # at the end we can also calculate the score of the project. S the score awarded for the project, if in time
        # points get subtracted if not completed before the best before date.
        # 1 point is subtracted for every day after the best before date. minimum score is 0.
        # contributors can still level up their skills even if project is finished too late.

        """3
        WebServer
        Bob Anna
        Logging
        Anna
        WebChat
        Maria Bob"""

        # loop over all projects
        for project in output_data.projects:
            if self.verbose:
                print(project)

            # all contributors need to have required level in role skills (either by themself or via mentor)
            for role, contributor in zip(project.roles, project.contributors):
                contributor_level = self.contributors[contributor.name][role.name]
                if contributor_level >= role.level:
                    continue
                elif (contributor_level + 1) == role.level:
                    # can a contributor mentor?
                    has_mentor = False
                    for mentor in project.contributors:
                        if self.contributors[mentor.name][role.name] >= role.level:
                            # yes, mentor is available
                            has_mentor = True
                            break
                    if not has_mentor:
                        # invalid project, because contributor does not have required skill and cannot be mentored
                        if self.verbose:
                            print(f'INVALID submission: {role.name=}, {contributor.name}')
                        return 0
                else:
                    # invalid project, because contributor does not have required skill
                    if self.verbose:
                        print(f'INVALID submission: {role.name=}, {contributor.name}')
                    return 0

            # check when all contributors are available.
            project_start_time = 0
            for contributor in project.contributors:
                # update project start time to max time when all contributors are available
                project_start_time = max(project_start_time, self.contributors_available_from[contributor.name])

            # execute the project: update available_from for all contributors. assign score.
            project_end_time = project_start_time + project.nr_of_days
            for contributor in project.contributors:
                self.contributors_available_from[contributor.name] = project_end_time

            # update skills of contributors
            for role, contributor in zip(project.roles, project.contributors):
                # increase level of skill if contributor level was equal or lower than required level
                if role.level <= self.contributors[contributor.name][role.name]:
                    self.contributors[contributor.name][role.name] += 1

            # check if project is completed before best before date
            if project_end_time < project.best_before:
                project_score = project.score
            else:
                project_score = max(0, project.score - (project_end_time - project.best_before))
            score += project_score

            # go to next project

        return score
