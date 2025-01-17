from datetime import date, datetime
from typing import List, Optional

import structlog
from fastapi import APIRouter
from pydantic_core import Url

from backend.schemas import AcquisitionDetails, CloudCoverageRatio, Coordinates
from backend.schemas.enums.mosaic_type import MosaicType
from backend.schemas.landsat.landsat_api import LandsatAPI
from backend.schemas.landsat.landsat_api_by_id import LandsatAPIById
from backend.schemas.landsat.landsat_api_by_search import LandsatAPIBySearch
from backend.schemas.landsat.landsat_item import LandsatItem
from backend.schemas.structures.tile_attributes import Mode, TileAttributes
from backend.utils.acquisitions_utils import AcquisitionsUtils
from backend.utils.geo_location_utils import WRS2Utils

logger = structlog.get_logger()

landsat_api_router = APIRouter()


@landsat_api_router.get("/search")
async def get_landsat_by_search(
    latitude: float,
    longitude: float,
    start_date: datetime,
    end_date: datetime,
    max_cloud_cover: CloudCoverageRatio = 0.2,
    max_items: int = 15,
    limit: int = 5,
) -> List[LandsatItem]:
    landsat_api = LandsatAPIBySearch(
        coordinates=Coordinates(lat=latitude, lon=longitude),
        start_date=start_date,
        end_date=end_date,
        max_cloud_cover=max_cloud_cover,
        max_items=max_items,
        limit=limit,
    )

    results = list(landsat_api.all_results)

    return results


@landsat_api_router.get("/id")
async def get_landsat_by_id(scene_id: str) -> LandsatItem:
    return LandsatAPIById(scene_id=scene_id).first_result


@landsat_api_router.get("/mosaic")
async def mosaic(scene_id: str, collection_id: str, mosaic_type: MosaicType) -> Url:
    return LandsatAPI.landsat_mosaic_builder(scene_id, collection_id, mosaic_type)


acquisitions = AcquisitionsUtils()
acquisitions.load_acquisitions()


@landsat_api_router.get("/get_acquisitions")
async def get_acquisitions(
    path: int,
    from_date: date,
    to_date: Optional[date] = None,
) -> List[tuple[str, date, AcquisitionDetails]]:
    return acquisitions.get_acquisitions(path, from_date, to_date=to_date)


@landsat_api_router.get("/get_scene")
async def get_scene(lat: float, lng: float, mode: Optional[Mode] = None) -> List[TileAttributes]:
    tiles = await WRS2Utils.get_wrs2_tiles(lat, lng, mode)
    return tiles
