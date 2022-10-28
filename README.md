# pymvil

A Multi-Variate Interpolation for Limits (PYMVIL)
- Helps to interpolate data over a number of dependent and independent variables. 
- Interpolation method of piecewise linear is available
- The algorithm assumes that the filter variable values in coords exist in data and are same

# Usage

See https://github.com/vamseeachanta/pymvil/blob/master/src/pymvil/tests/test_mvil_csv_no_monotonic_trend.py

# Improvements

**#TODO**
- Further visualizations can be added to verify data results
    - Parameter (and detailed) charts can be converted to 3D charts to include the independent variable trends to verify output 
- Response of independent variable defined as greater than and less than (ge, le) can help create provide more flexibility to module. Currently acceptance trend is determined by assuming the first value of the group (irrespective of greater or lesser than limit) is acceptable.




### References


https://www.geeksforgeeks.org/3d-scatter-plot-using-plotly-in-python/
