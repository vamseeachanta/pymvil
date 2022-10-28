import os
from pathlib import Path


def save_result_as_csv(mvil_config_csv, result_df):
    result_dir = os.path.join(os.getcwd(), 'src', 'pymvil', 'tests', 'result')
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    result_basename = Path(mvil_config_csv['data']).stem
    result_df.to_csv(os.path.join(result_dir, result_basename + '_result.csv'),
                     index=False)
