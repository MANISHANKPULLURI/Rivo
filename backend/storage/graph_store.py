import os

class GraphStore:
    """
    Knowledge: Manages the storage of generated financial charts.
    """
    def __init__(self):
        self.path = os.getenv("GRAPH_STORAGE_PATH")
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def save_chart(self, fig, filename: str):
        """Saves a Plotly or Matplotlib figure to the storage folder"""
        full_path = os.path.join(self.path, filename)
        fig.write_image(full_path) # Assumes using Plotly for pro-look
        return full_path