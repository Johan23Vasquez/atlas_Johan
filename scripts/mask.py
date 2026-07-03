import xarray as xr
import geopandas as gpd
import rioxarray


MEXICO_SHP = "data/INEGI/00ent.shp"


def load_mexico_geometry(dissolve=True, crs="EPSG:4326"):
    """
    Carga automáticamente el shapefile de México desde la ruta fija.
    """

    shp = gpd.read_file(MEXICO_SHP)
    shp = shp.to_crs(crs)

    if dissolve:
        shp = shp.dissolve()

    return shp


def prepare_dataset(ds, crs="EPSG:4326"):
    """
    Asigna CRS al NetCDF para compatibilidad con rasterio.
    """
    return ds.rio.write_crs(crs)


def clip_to_mexico(ds, mexico_gdf, drop=False):
    """
    Recorta el NetCDF usando el polígono de México.
    """
    return ds.rio.clip(
        mexico_gdf.geometry,
        mexico_gdf.crs,
        drop=drop
    )


def mask_netcdf_to_mexico(
    nc_path,
    output_path,
    drop=False,
    crs="EPSG:4326"
):
    """
    Pipeline completo:
    NetCDF → clip a México → NetCDF recortado
    """

    # 1. abrir NetCDF
    ds = xr.open_dataset(nc_path)

    # 2. cargar México automáticamente
    mexico = load_mexico_geometry(crs=crs)

    # 3. preparar CRS del raster
    ds = prepare_dataset(ds, crs=crs)

    # 4. clip
    ds_mexico = clip_to_mexico(ds, mexico, drop=drop)

    # 5. guardar resultado
    ds_mexico.to_netcdf(output_path)

    return ds_mexico


#uso posible del script

# from mask_mexico import mask_netcdf_to_mexico

# ds_mexico = mask_netcdf_to_mexico(
#     nc_path="2022.nc",
#     output_path="2022_mexico.nc"
# )

# Función unica

MEXICO_SHP = "data/INEGI/00ent.shp"


def load_mexico_geometry(dissolve=True, crs="EPSG:4326"):
    """
    Carga automáticamente el shapefile de México desde la ruta fija.
    """

    shp = gpd.read_file(MEXICO_SHP)
    shp = shp.to_crs(crs)

    if dissolve:
        shp = shp.dissolve()

    return shp


def prepare_dataset(ds, crs="EPSG:4326"):
    """
    Asigna CRS al NetCDF para compatibilidad con rasterio.
    """
    return ds.rio.write_crs(crs)


def clip_to_mexico(ds, mexico_gdf, drop=False):
    """
    Recorta el NetCDF usando el polígono de México.
    """
    return ds.rio.clip(
        mexico_gdf.geometry,
        mexico_gdf.crs,
        drop=drop
    )