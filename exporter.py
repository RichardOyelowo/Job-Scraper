from datetime import datetime
import pandas as pd
import os


def export_to_csv(jobs, output_dir="output"):
    """ Export jobs details to csv """

    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(jobs)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"jobs_{timestamp}.csv")

    df.to_csv(file_path, index=False)

    return file_path
