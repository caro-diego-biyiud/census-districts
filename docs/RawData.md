# Raw Data

- **SECC_CE_20250101.sph** - Main geometry file
- **SECC_CE_20250101.dbf** - Attribute data
- **SECC_CE_20250101.prj** - Projection/coordinate system information
- **SECC_CE_20250101.shx** - Shape index file
- **SECC_CE_20250101.sbn/.sbx** - Spatial index files
- **SECC_CE_20250101.CPG** - Code page file

It only needs to be **references the .sph** file, GeoPandas will automatically find and use the others associated files, as long as they're in the same directory with the same base name.