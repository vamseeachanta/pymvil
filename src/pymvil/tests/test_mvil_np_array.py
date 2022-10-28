import pytest
import numpy as np
from pymvil.mvil import mvil

data = np.array([[12, 127.1, 2800], [12, 132.3, 3400.23], [12, 154.3, 5000.1],
                 [12, 171.1, 6880.7], [12, 190.7, 9711.1], [12, 195.3, 10011.2],
                 [14, 113.1, 2420], [14, 125.3, 3320], [14, 133.3, 4129.91],
                 [14, 155.1, 6287.17], [14, 187.7, 10800.34],
                 [14, 197.3, 13076.5]])

coords = np.array([[12.2, 122.1], [12.4, 137.3], [12.5, 154.9], [12.6, 171.4],
                   [12.7, 192.6], [12.8, 198.5]])

mvil_config = {
    'data_type': 'np.array',
    'data': data,
    'data_variables': ['c', 'speed', 'power'],
    'interpolation_coords': coords,
    'interpolation_coords_variables': ['c', 'speed'],
    'method': {
        'in_range': 'linear',
        'out_of_range': 'nearest'
    }
}
result = mvil(mvil_config=mvil_config)
print(result)
assert result[0] == pytest.approx(3320, abs=0.5)
assert result[1] == pytest.approx(3895.2, abs=0.5)
assert result[2] == pytest.approx(5366.6, abs=0.5)
assert result[3] == pytest.approx(7408.7, abs=0.5)
assert result[4] == pytest.approx(10791.8, abs=0.5)
assert result[5] == pytest.approx(13076.5, abs=0.5)

mvil_config2 = {
    'data_type': 'np.array',
    'data': data,
    'data_variables': ['c', 'speed', 'power'],
    'interpolation_coords': coords,
    'interpolation_coords_variables': ['c', 'speed'],
    'method': {
        'in_range': 'linear',
        'out_of_range': None
    }
}
result = mvil(mvil_config=mvil_config2)
print(result)
assert np.isnan(result[0])
assert result[1] == pytest.approx(3895.2, abs=0.5)
assert result[2] == pytest.approx(5366.6, abs=0.5)
assert result[3] == pytest.approx(7408.7, abs=0.5)
assert result[4] == pytest.approx(10791.8, abs=0.5)
assert np.isnan(result[5])
