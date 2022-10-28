import pytest
import pandas as pd

from pymvil.mvil import mvil
from pymvil.save_result_as_csv import save_result_as_csv

mvil_config_csv_array = [{
    'data_type': 'csv',
    'data': 'src/pymvil/tests/test_data/1500m_08ppg_0_off_hs_data.csv',
    'interpolation_coords': 'src/pymvil/tests/test_data/1500m_hs_coords.csv',
    'method': {
        'in_range': 'linear',
        'out_of_range': None
    },
    'fill_value': 2.35,
    'visualizations': False
}, {
    'data_type': 'csv',
    'data': 'src/pymvil/tests/test_data/1500m_14ppg_0_off_hs_data.csv',
    'interpolation_coords': 'src/pymvil/tests/test_data/1500m_hs_coords.csv',
    'method': {
        'in_range': 'linear',
        'out_of_range': None
    },
    'fill_value': 2.35,
    'visualizations': False
}]

for mvil_config_csv in mvil_config_csv_array:
    data_df = pd.read_csv(mvil_config_csv['data'])
    coords_df = pd.read_csv(mvil_config_csv['interpolation_coords'])
    data_variables = list(data_df.columns)
    coords_variables = list(coords_df.columns)
    output_variable = list(set(data_variables) - set(coords_variables))[0]

    independent_variables_for_interpolation = coords_variables[3:]
    filter_variables = coords_variables[0:3]

    result_df = coords_df.copy()
    indep_var_result_columns = [
        indep_var + '_' + output_variable + '_result'
        for indep_var in independent_variables_for_interpolation
    ]
    for indep_var in independent_variables_for_interpolation:
        coord_variables_for_indep_var = filter_variables + [indep_var]
        data_variables_for_indep_var = coord_variables_for_indep_var + [
            output_variable
        ]

        data = data_df[data_variables_for_indep_var].to_numpy()
        coords = coords_df[coord_variables_for_indep_var].to_numpy()

        mvil_config = {
            'data_type': 'np.array',
            'data': data,
            'data_variables': data_variables_for_indep_var,
            'interpolation_coords': coords,
            'interpolation_coords_variables': coord_variables_for_indep_var,
            'method': {
                'in_range': mvil_config_csv['method']['in_range'],
                'out_of_range': mvil_config_csv['method']['out_of_range']
            },
            'fill_value': mvil_config_csv['fill_value']
        }
        result = mvil(mvil_config=mvil_config)

        indep_var_result_column = indep_var + '_' + output_variable + '_result'
        result_df[indep_var_result_column] = result

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
                'title':
                    f'Project Title <br> Interpolation Result - {indep_var}'
            }

            result_dir = os.path.join(os.getcwd(), 'src', 'pymvil', 'tests',
                                      'result')
            result_dir_detailed = os.path.join(os.getcwd(), 'src', 'pymvil',
                                               'tests', 'result', 'detailed')
            if not os.path.exists(result_dir):
                os.mkdir(result_dir)
            if not os.path.exists(result_dir_detailed):
                os.mkdir(result_dir_detailed)
            result_basename = Path(mvil_config_csv['data']).stem

            for groupby_value in groupby_values:
                groupby_name = groupby_col + str(groupby_value)
                result_df_temp = result_df[result_df[groupby_col] ==
                                           groupby_value]
                groupby_col_2 = filter_variables[2]
                groupby_values_2 = list(result_df_temp[groupby_col_2].unique())

                data_2 = []
                for groupby_value_2 in groupby_values_2:
                    result_df_temp_2 = result_df_temp[
                        result_df_temp[groupby_col_2] == groupby_value_2]
                    groupby_name_2 = groupby_col_2 + str(groupby_value_2)
                    x = list(result_df_temp_2[x_col])
                    y = list(result_df_temp_2[y_col])
                    data.append(
                        go.Scatter(name=groupby_name + groupby_name_2, x=x,
                                   y=y))
                    data_2.append(go.Scatter(name=groupby_name_2, x=x, y=y))

                filename_2 = result_basename + '_' + groupby_name
                fig = go.Figure(data=data_2, layout=layout)
                filename_2 = result_basename + '_' + groupby_name + '_' + indep_var
                fig.write_html(
                    os.path.join(result_dir_detailed, filename_2 + '.html'))

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
