# This is a sample Python script.
import geopandas as gpd
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import shapely
import pandas as pd

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    edges_gdf = pd.DataFrame({
        'id': [1, 2, 3],
        'geometry': [shapely.geometry.Point(1, 2), shapely.geometry.Point(3, 4), shapely.geometry.Point(5, 6)],
        'attributes': [{"name": "A", "value": 1}, {"name": "B", "value": 2}, {"name": "C", "value": 3}]
    })

    edges_gdf = edges_gdf.join(edges_gdf['attributes'].apply(pd.Series))

    print(edges_gdf)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
