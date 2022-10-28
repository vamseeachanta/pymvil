import pandas as pd
import os
from pathlib import Path

import plotly.graph_objects as go
from pymvil.no_monotonic_trend_analysis import get_variable_array_groups


def create_result_folder():
    result_dir = os.path.join(os.getcwd(), 'src', 'pymvil', 'tests', 'result')
    result_dir_detailed = os.path.join(os.getcwd(), 'src', 'pymvil', 'tests',
                                       'result', 'detailed')
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    if not os.path.exists(result_dir_detailed):
        os.mkdir(result_dir_detailed)
    return result_dir, result_dir_detailed


def create_visualizations(mvil_config_csv, result_df):
    result_dir, result_dir_detailed = create_result_folder()

    review_interpolation_result(mvil_config_csv, result_df, result_dir,
                                result_dir_detailed)


def review_interpolation_result(mvil_config_csv,
                                result_df,
                                result_dir,
                                result_dir_detailed,
                                groupby_col_index=1):

    data_df = pd.read_csv(mvil_config_csv['data'])
    coords_df = pd.read_csv(mvil_config_csv['interpolation_coords'])

    output_variable, independent_variables_for_interpolation, filter_variables = get_variable_array_groups(
        data_df, coords_df)

    for indep_var_index in range(0,
                                 len(independent_variables_for_interpolation)):
        indep_var = independent_variables_for_interpolation[indep_var_index]
        indep_var_result_column = indep_var + '_' + output_variable + '_result'

        x_col = filter_variables[0]
        y_col = indep_var_result_column

        create_group_chart(
            mvil_config_csv,
            result_df,
            result_dir,
            result_dir_detailed,
            groupby_col_index,
            filter_variables,
            output_variable,
            x_col,
            y_col,
            indep_var,
        )

    y_col = 'operating_envelope'
    create_group_chart(
        mvil_config_csv,
        result_df,
        result_dir,
        result_dir_detailed,
        groupby_col_index,
        filter_variables,
        output_variable,
        x_col,
        y_col,
        'operating_envelope',
    )


def create_group_chart(
    mvil_config_csv,
    result_df,
    result_dir,
    result_dir_detailed,
    groupby_col_index,
    filter_variables,
    output_variable,
    x_col,
    y_col,
    indep_var,
):

    result_basename = Path(mvil_config_csv['interpolation_coords']).stem
    groupby_col = filter_variables[groupby_col_index]
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
    if y_col != 'operating_envelope':
        fig.write_html(os.path.join(result_dir_detailed, filename + '.html'))
    else:
        fig.write_html(os.path.join(result_dir, filename + '.html'))
