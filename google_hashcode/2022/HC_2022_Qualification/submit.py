import os

from valcon import SubmissionCreator

if __name__ == '__main__':
    this_path = os.path.abspath(os.path.dirname(__file__))
    submission_creator = SubmissionCreator()
    submission_creator.create_zip(this_path)
