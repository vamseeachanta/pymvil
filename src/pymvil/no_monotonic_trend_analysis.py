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
