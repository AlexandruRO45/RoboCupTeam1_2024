import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from controllers.base.base_supervisor import BaseSupervisor
supervisor = BaseSupervisor()
supervisor.run()

# import pandas as pd
# # from functions import write_data, draw_pizza, draw_heat

# class Supervisor(BaseSupervisor):
#     def __init__(self, file_name):
#         super().__init__()
#         self.file_name = file_name
#         self.robot_names = super().RobotList()  # Replace with your specific logic to retrieve robot names

#     def logging(self):
#         data = super().get_data()
#         write_data(self.file_name, data)

#     def possession_percentage(self):
#         data = pd.read_csv(self.file_name)
#         possession_counts = data['robot'].value_counts()
#         possession_percentages = possession_counts / len(data) * 100
#         draw_pizza(possession_percentages, self.robot_names, "possession_percentage.png")

#     def passing_percentage(self):
#         data = pd.read_csv(self.file_name)
#         # Placeholder: Implement your logic to identify valid passing events
#         passing_percentages = {}  # Placeholder: Calculate passing percentages for each robot
#         draw_pizza(passing_percentages, self.robot_names, "passing_percentage.png")

#     def interrupt_percentage(self):
#         data = pd.read_csv(self.file_name)
#         # Placeholder: Implement your logic to identify valid interception events
#         interception_percentages = {}  # Placeholder: Calculate interception percentages for each robot
#         draw_pizza(interception_percentages, self.robot_names, "defence_percentage.png")

#     def create_heat(self):
#         data = pd.read_csv(self.file_name)
#         pressure_data = data[['pressure1', 'pressure2']]
#         draw_heat(pressure_data, "heatmap.png")

#     def run(self):
#         while super().step(TIME_STEP) != -1:
#             self.logging()
#             self.possession_percentage()
#             self.passing_percentage()
#             self.interrupt_percentage()
#             self.create_heat()