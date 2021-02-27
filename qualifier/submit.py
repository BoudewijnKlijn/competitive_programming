import os
import zipfile


def zip_submission():
    THIS_PATH = os.path.abspath(os.path.dirname(__file__))
    print(f'Zipping {THIS_PATH}')

    zf = zipfile.ZipFile(os.path.join(THIS_PATH, 'outputs', 'submission.zip'), mode='w')
    for file_name in os.listdir(THIS_PATH):
        if os.path.isfile(os.path.join(THIS_PATH, file_name)):
            zf.write(os.path.join(THIS_PATH, file_name), file_name)
    zf.close()
    print('Zipped')


if __name__ == '__main__':
    zip_submission()
