import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../..'
PROJECT_DIR = os.path.normpath(PROJECT_DIR)
PROJECT_NAME = os.path.basename(PROJECT_DIR)

if __name__ == "__main__":
    print(PROJECT_DIR, PROJECT_NAME)


