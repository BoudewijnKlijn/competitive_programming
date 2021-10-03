import os
import zipfile
import glob


def zip_submission():
    THIS_PATH = os.path.abspath(os.path.dirname(__file__))
    print(f'Zipping {THIS_PATH}')

    zf = zipfile.ZipFile(os.path.join(THIS_PATH, 'outputs', 'submission.zip'), mode='w')
    for file_name in glob.glob(THIS_PATH):
        # if os.path.isfile(os.path.join(THIS_PATH, file_name)):
        if not all(dir_name not in file_name for dir_name in ['inputs', 'outputs', '__pycache__']):
            zf.write(os.path.join(THIS_PATH, file_name), file_name)

    zf.close()
    print('Zipped')


if __name__ == '__main__':
    zip_submission()
