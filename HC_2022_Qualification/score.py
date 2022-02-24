from HC_2022_Qualification.problem_data import ProblemData
from HC_2022_Qualification.solution import Solution
from valcon.scorer import Scorer


class Score(Scorer):
    def __init__(self, input_data: ProblemData):
        self.available_from = input_data.available_from  # from which time are contributors available. all start at 0


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
        for project in output_data:

            project_start_time = 0

            for skill, level in project.skills:

                # get all contributors for this project
                for contributor in project.contributors:

                    # check if contributor has required skill, else invalid input, return 0
                    if contributor.skill >= project.required_skill:
                        continue
                    elif (contributor.skill + 1) == project.required_skill:
                        # mentor has to be on project
                        for mentor in project.contributors:
                            if mentor.skill >= project.required_skill:
                        return 0

                    # update project start time to max time when all contributors are available
                    project_start_time = max(project_start_time, self.available_from[contributor.name])

                # execute the project
                project_end_time = project_start_time + project.duration

                # update skills of

