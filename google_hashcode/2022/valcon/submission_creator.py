import glob
import os
import zipfile


class SubmissionCreator:
    def __init__(self, include_package=True) -> None:
        self.include_package = include_package
        self.package_path = os.path.abspath(os.path.dirname(__file__))

    @staticmethod
    def _in_blacklist(path) -> bool:
        dir_blacklist = ['input', 'output', '__pycache__']
        for text in dir_blacklist:
            directory = os.path.split(path)[0]
            if text in directory:
                return True
        return False

    def create_zip(self, path) -> None:

        print(f'Zipping {path}')

        if not os.path.exists(os.path.join(path, 'output')):
            os.mkdir(os.path.join(path, 'output'))

        with zipfile.ZipFile(os.path.join(path, 'output', 'submission.zip'), mode='w') as zf:
            for file_name in glob.glob(os.path.join(path, '**/*'), recursive=True):
                if not self._in_blacklist(file_name):
                    print(f'Adding {file_name}')
                    zf.write(os.path.join(path, file_name), file_name)

            if self.include_package:
                for file_name in glob.glob(os.path.join(self.package_path, '**/*'), recursive=True):
                    if not self._in_blacklist(file_name):
                        print(f'Adding {file_name}')
                        zf.write(os.path.join(self.package_path, file_name), file_name)

        print('Zipped')
