# Terrain to .STL format

1. Download the .asc file with the digital terrain model (e.g. <https://mapy.geoportal.gov.pl/imap/Imgp_2.html?gpmap=gp0>, on the left: data download -> WCS -> Digital terrain model - Arc/info ASCII grid -> Draw area -> Download file).
2. In the .asc file, replace the `dx` and `dy` lines with the following lines (if needed):

   ```asc
   cellsize    1.0001
   NODATA_value  0
   ```

3. Blender: Install the BlenderGIS library (<https://github.com/domlysz/BlenderGIShttps://github.com/domlysz/BlenderGIS>).
4. GIS -> Import -> ESRI ASCII Grid (asc).
5. Scripting -> paste or load the `./script.py` file, press RUN and wait (this can take very long).
6. Export -> .stl.
