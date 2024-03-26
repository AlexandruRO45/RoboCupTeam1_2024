import os

class MotionPath:
    def __init__(self, motion_folder):
        self.motion_folder = motion_folder
        self.motion_files = self.load_motion_files()

    def load_motion_files(self):
        motion_files = []
        for file in os.listdir(self.motion_folder):
            if file.endswith(".motion"):
                motion_files.append(file)
        return motion_files

    def get_motion_file(self, motion_name):
        motion_file = os.path.join(self.motion_folder, motion_name)
        if motion_file in self.motion_files:
            return motion_file
        else:
            raise ValueError("Motion file not found.")

# Example usage
motion_folder = "/path/to/plugins/motion"
motion_path = MotionPath(motion_folder)

# Get a specific motion file
motion_file = motion_path.get_motion_file("walk.motion")
print(motion_file)