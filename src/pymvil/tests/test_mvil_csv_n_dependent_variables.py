import pytest
import pandas as pd

from pymvil.mvil import mvil
from pymvil.save_result_as_csv import save_result_as_csv

mvil_config_csv = {
    'data_type': 'csv',
    'data': 'src/pymvil/tests/test_data/hs_data.csv',
    'interpolation_coords': 'src/pymvil/tests/test_data/hs_coords.csv',
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

output_variable = list(set(data_variables) - set(coords_variables))[0]
result_df = coords_df.copy()
result_df[output_variable + '_result'] = result

save_result_as_csv(mvil_config_csv, result_df)
print(result_df)

# assert result[0] == pytest.approx(3320, abs=0.5)
