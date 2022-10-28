import pytest
import pandas as pd

from pymvil.mvil import mvil
from pymvil.save_result_as_csv import save_result_as_csv

mvil_config_csv = {
    'data_type': 'csv',
    'data': 'src/pymvil/tests/test_data/power_data.csv',
    'interpolation_coords': 'src/pymvil/tests/test_data/power_coords.csv',
    'method': {
        'in_range': 'linear',
        'out_of_range': 'nearest'
    }
}

data_df = pd.read_csv(mvil_config_csv['data'])
coords_df = pd.read_csv(mvil_config_csv['interpolation_coords'])
data_variables = list(data_df.columns)
coords_variables = list(coords_df.columns)
data = data_df.to_numpy()
coords = coords_df.to_numpy()
output_variable = list(set(data_variables) - set(coords_variables))[0]

result_df = coords_df.copy()
mvil_config = {
    'data_type': 'np.array',
    'data': data,
    'data_variables': data_variables,
    'interpolation_coords': coords,
    'interpolation_coords_variables': coords_variables,
    'method': {
        'in_range': 'linear',
        'out_of_range': 'nearest'
    }
}

result = mvil(mvil_config=mvil_config)
result_df[output_variable + '_result'] = result

save_result_as_csv(mvil_config_csv, result_df)
print(result_df)

assert result[0] == pytest.approx(3320, abs=0.5)
assert result[1] == pytest.approx(3895.2, abs=0.5)
assert result[2] == pytest.approx(5366.6, abs=0.5)
assert result[3] == pytest.approx(7408.7, abs=0.5)
assert result[4] == pytest.approx(10791.8, abs=0.5)
assert result[5] == pytest.approx(13076.5, abs=0.5)
