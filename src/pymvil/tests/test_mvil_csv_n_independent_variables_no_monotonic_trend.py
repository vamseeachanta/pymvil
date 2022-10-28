import pytest
import pandas as pd
import piecewise_regression

import numpy.polynomial.polynomial as poly
from pymvil.mvil import mvil
from pymvil.save_result_as_csv import save_result_as_csv
from pymvil.no_monotonic_trend_analysis import get_variable_array_groups, get_filtered_df

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

data_df = pd.read_csv(mvil_config_csv['data'])
coords_df = pd.read_csv(mvil_config_csv['interpolation_coords'])

output_variable, independent_variables_for_interpolation, filter_variables = get_variable_array_groups(
    data_df, coords_df)

result_df = coords_df.copy()
indep_var_result_columns = [
    indep_var + '_' + output_variable + '_result'
    for indep_var in independent_variables_for_interpolation
]

for coords_df_index in range(0, len(coords_df)):
    coord_df = coords_df.loc[[coords_df_index], :]
    filtered_df = get_filtered_df(data_df, filter_variables, coord_df)
    for indep_var_index in range(0,
                                 len(independent_variables_for_interpolation)):
        indep_var = independent_variables_for_interpolation[indep_var_index]
        coord_variables_for_indep_var = [indep_var]
        data_variables_for_indep_var = coord_variables_for_indep_var + [
            output_variable
        ]

        data = filtered_df[data_variables_for_indep_var].to_numpy()
        coord = coord_df[coord_variables_for_indep_var].to_numpy()

        mvil_config = {
            'data_type': 'np.array',
            'data': data,
            'data_variables': data_variables_for_indep_var,
            'interpolation_coords': coord,
            'interpolation_coords_variables': coord_variables_for_indep_var,
            'method': {
                'in_range': mvil_config_csv['method']['in_range'],
                'out_of_range': mvil_config_csv['method']['out_of_range']
            },
            'fill_value': mvil_config_csv['fill_value']
        }
        if mvil_config['method']['in_range'] == 'piecewise_linear':
            x_new = coord_df[indep_var].iloc[0]
            x_1 = filtered_df[indep_var].iloc[0]
            check_fill_value_df = filtered_df[filtered_df[indep_var] == x_new]
            if len(check_fill_value_df) > 0:
                y_new = check_fill_value_df[output_variable].iloc[0]
            else:
                if x_1 > x_new:
                    check_fill_value_df = filtered_df[
                        filtered_df[indep_var] < x_new]
                else:
                    check_fill_value_df = filtered_df[
                        filtered_df[indep_var] >= x_new]
                if len(check_fill_value_df) <= 1:
                    y_new = mvil_config['fill_value']
                else:
                    end_index = check_fill_value_df.index[0]
                    x = list(filtered_df[indep_var].loc[end_index -
                                                        1:end_index])
                    y = list(filtered_df[output_variable].loc[end_index -
                                                              1:end_index])
                    coefs = poly.polyfit(x, y, 2)
                    y_new = poly.polyval(x_new, coefs)
        else:
            y_new = mvil(mvil_config=mvil_config)[0][0]

        indep_var_result_column = indep_var + '_' + output_variable + '_result'
        result_df.loc[[coords_df_index], [indep_var_result_column]] = y_new

if mvil_config_csv['visualizations']:
    import os
    from pathlib import Path
    import plotly.graph_objects as go

    x_col = filter_variables[0]
    y_col = indep_var_result_column
    groupby_col = filter_variables[1]
    groupby_values = list(result_df[groupby_col].unique())
    data = []
    layout = {
        'xaxis': {
            'title': x_col
        },
        'yaxis': {
            'title': output_variable
        },
        'title': f'Project Title <br> Interpolation Result - {indep_var}'
    }

    result_dir = os.path.join(os.getcwd(), 'src', 'pymvil', 'tests', 'result')
    result_dir_detailed = os.path.join(os.getcwd(), 'src', 'pymvil', 'tests',
                                       'result', 'detailed')
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    if not os.path.exists(result_dir_detailed):
        os.mkdir(result_dir_detailed)
    result_basename = Path(mvil_config_csv['interpolation_coords']).stem

    for groupby_value in groupby_values:
        groupby_name = groupby_col + str(groupby_value)
        result_df_temp = result_df[result_df[groupby_col] == groupby_value]
        groupby_col_2 = filter_variables[2]
        groupby_values_2 = list(result_df_temp[groupby_col_2].unique())

        data_2 = []
        for groupby_value_2 in groupby_values_2:
            result_df_temp_2 = result_df_temp[result_df_temp[groupby_col_2] ==
                                              groupby_value_2]
            groupby_name_2 = groupby_col_2 + str(groupby_value_2)
            x = list(result_df_temp_2[x_col])
            y = list(result_df_temp_2[y_col])
            data.append(go.Scatter(name=groupby_name + groupby_name_2, x=x,
                                   y=y))
            data_2.append(go.Scatter(name=groupby_name_2, x=x, y=y))

        filename_2 = result_basename + '_' + groupby_name
        fig = go.Figure(data=data_2, layout=layout)
        filename_2 = result_basename + '_' + groupby_name + '_' + indep_var
        fig.write_html(os.path.join(result_dir_detailed, filename_2 + '.html'))

    fig = go.Figure(data=data, layout=layout)
    filename = result_basename + '_' + indep_var
    fig.write_html(os.path.join(result_dir, filename + '.html'))

save_result_as_csv(mvil_config_csv, result_df)
print(result_df)

# assert result[0] == pytest.approx(3320, abs=0.5)
# assert result[1] == pytest.approx(3895.2, abs=0.5)
# assert result[2] == pytest.approx(5366.6, abs=0.5)
# assert result[3] == pytest.approx(7408.7, abs=0.5)
# assert result[4] == pytest.approx(10791.8, abs=0.5)
# assert result[5] == pytest.approx(13076.5, abs=0.5)
