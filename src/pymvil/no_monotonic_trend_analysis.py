import pytest
import pandas as pd
import piecewise_regression

import numpy.polynomial.polynomial as poly
from pymvil.mvil import mvil


def get_variable_array_groups(data_df, coords_df):
    data_variables = list(data_df.columns)
    coords_variables = list(coords_df.columns)
    output_variable_array = list(set(data_variables) - set(coords_variables))
    if len(output_variable_array) > 1:
        raise (
            "More than 1 output variable found {output_variable_array}. Can not perform mvil interpolation"
        )
    output_variable = list(set(data_variables) - set(coords_variables))[0]

    independent_variables_for_interpolation = coords_variables[3:]
    filter_variables = coords_variables[0:3]
    return output_variable, independent_variables_for_interpolation, filter_variables


def get_filtered_df(data_df, filter_variables, coord_df):
    filtered_df = data_df.copy()
    for filter_variable in filter_variables:
        filtered_df = filtered_df[filtered_df[filter_variable] ==
                                  coord_df[filter_variable].iloc[0]].copy()
        if len(filtered_df) > 0:
            pass
        else:
            raise (
                f"Data set does not have values for filter variables. Monotonic trend analysis can not be performed"
            )

    return filtered_df


def no_monotonic_trend_analysis(mvil_config_csv):
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
        for indep_var_index in range(
                0, len(independent_variables_for_interpolation)):
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
                check_fill_value_df = filtered_df[filtered_df[indep_var] ==
                                                  x_new]
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
                        coefs = poly.polyfit(x, y, 1)
                        y_new = poly.polyval(x_new, coefs)
            else:
                y_new = mvil(mvil_config=mvil_config)[0][0]

            indep_var_result_column = indep_var + '_' + output_variable + '_result'
            result_df.loc[[coords_df_index], [indep_var_result_column]] = y_new

    result_df['operating_envelope'] = result_df[indep_var_result_columns].min(
        axis=1)

    return result_df
