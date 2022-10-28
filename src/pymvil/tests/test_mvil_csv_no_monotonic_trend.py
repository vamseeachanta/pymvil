import pytest

from pymvil.save_result_as_csv import save_result_as_csv
from pymvil.no_monotonic_trend_analysis import no_monotonic_trend_analysis
from pymvil.create_visualizations import create_visualizations

mvil_config_csv = {
    'data_type': 'csv',
    'data': 'src/pymvil/tests/test_data/hs_data_full.csv',
    'interpolation_coords': 'src/pymvil/tests/test_data/hs_coords_full.csv',
    'method': {
        'in_range': 'piecewise_linear',
        'out_of_range': None
    },
    'fill_value': 2.35,
    'visualizations': True
}

result_df = no_monotonic_trend_analysis(mvil_config_csv)

save_result_as_csv(mvil_config_csv, result_df)
print(result_df)

if mvil_config_csv['visualizations']:
    create_visualizations(mvil_config_csv, result_df)

assert result_df['operating_envelope'].iloc[-1] == pytest.approx(1.046, abs=0.1)
