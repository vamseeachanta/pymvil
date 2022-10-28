import numpy as np
from scipy.interpolate import griddata


def mvil(mvil_config):

    method = mvil_config['method']['in_range']
    grid_data, output_in_data = get_transformed_data(mvil_config)
    interpolation_coords = mvil_config['interpolation_coords']
    fill_value = mvil_config.get('fill_value', np.nan)
    result = griddata(grid_data,
                      output_in_data,
                      interpolation_coords,
                      method=method,
                      fill_value=fill_value)

    if mvil_config['method']['out_of_range'] == 'nearest':
        method = 'nearest'
        result_nearest = griddata(grid_data,
                                  output_in_data,
                                  interpolation_coords,
                                  method=method)

        print(result_nearest)

        for result_index in range(0, len(result)):
            if np.isnan(result[result_index]):
                result[result_index] = result_nearest[result_index]

    print(
        f"Using in range method: {mvil_config['method']['in_range']}; out of range method: {mvil_config['method']['out_of_range']}"
    )

    return result


def get_transformed_data(mvil_config):
    data_variables = mvil_config['data_variables']
    interpolation_coords_variables = mvil_config[
        'interpolation_coords_variables']

    interpolation_coords_variables_index_in_data = [
        data_variables.index(item) for item in interpolation_coords_variables
    ]

    output_variable = list(
        set(data_variables) - set(interpolation_coords_variables))[0]
    print(f"Output variable for coords is: {output_variable}")
    output_index = data_variables.index(output_variable)

    data = mvil_config['data']
    grid_data = [
        item[interpolation_coords_variables_index_in_data] for item in data
    ]
    output_in_data = mvil_config['data'][:, output_index]

    return grid_data, output_in_data
