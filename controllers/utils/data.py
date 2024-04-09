import numpy as np
import math
import csv
from mplsoccer import PyPizza, FontManager

import matplotlib.pyplot as plt

class ChartDrawer:
    def __init__(self, params, values, file_name, stat_type):
        self.params = params
        self.values = values
        self.file_name = file_name
        self.stat_type = stat_type

    def draw_pizza(self):
        # Create a PyPizza instance
        pizza = PyPizza(
            params=self.params,                  # List of labels for each pizza slice
            values=self.values,                  # List of numerical values corresponding to each slice
            background_color="#FFFFFF",     # Background color of the pizza chart
            straight_line_color="#000000",  # Color of the straight lines separating the slices
            straight_line_lw=1.0,           # Line width of the straight lines
            last_circle_color="#000000",    # Color of the last circle in the center of the pizza
            last_circle_lw=1.0,             # Line width of the last circle
            other_circle_color="#000000",   # Color of the other circles in the center of the pizza
            other_circle_lw=1.0,            # Line width of the other circles
            inner_circle_ratio=0.2,         # Ratio of the inner circle radius to the outer circle radius
            outer_circle_ratio=1.0,         # Ratio of the outer circle radius to the pizza radius
            straight_line_color_code=True   # Use color codes for straight lines
        )

        # Plot the pizza chart
        fig, ax = plt.subplots(figsize=(8, 8))
        pizza.draw(ax)

        # Customize the appearance
        font_manager = FontManager()
        font_properties = font_manager.prop
        plt.title(f"{self.stat_type} Distribution", fontproperties=font_properties, fontsize=16)
        plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1), prop=font_properties)

        # Save the image
        plt.savefig(self.file_name, dpi=300, bbox_inches="tight")
        plt.close(fig)

    def draw_pie_chart(self):
        # Create a pie chart with labels and autopct for percentages
        plt.pie(self.values, labels=self.params, autopct="%1.1f%%", startangle=90)

        # Add a title and customize the plot
        plt.title(f"ROBOCUP - {self.stat_type} Percentage\nRed Team vs Blue Team")
        plt.axis('equal')  # Equal aspect ratio ensures a circular pie chart
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))  # Legend in top left corner

        # Customize colors and fonts (replace with desired styles)
        plt.gca().set_prop_cycle('color', ['#d70232', '#1a78cf', '#f7f7f7', '#cccccc'])  # Example color cycle
        plt.gca().set_title_fontsize(14)
        plt.gca().set_xlabel_fontsize(12)
        plt.gca().set_ylabel_fontsize(12)

        # Save the plot as an image
        plt.savefig(self.file_name)
        plt.close()  # Close the plot to avoid memory issues

    def draw_heatmap(self):
        # Create a heatmap using the values
        plt.imshow(self.values, cmap='hot', interpolation='nearest')

        # Add a colorbar to the heatmap
        plt.colorbar()

        # Add labels to the axes
        plt.xlabel('Pressure 1')
        plt.ylabel('Pressure 2')

        # Add a title to the plot
        plt.title('Pressure Heatmap')

        # Save the plot as an image
        plt.savefig(self.file_name)
        plt.close()  # Close the plot to avoid memory issues