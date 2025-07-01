from pyproj import Transformer

# Координаты в EPSG:3857
xmin, ymin = 3373549.3298764327, 8388032.7590
xmax, ymax = 3375868.4019, 8389404.544040648

transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

min_lon, min_lat = transformer.transform(xmin, ymin)
max_lon, max_lat = transformer.transform(xmax, ymax)

print("SouthWest (min_lat, min_lon):", min_lat, min_lon)
print("NorthEast (max_lat, max_lon):", max_lat, max_lon)
