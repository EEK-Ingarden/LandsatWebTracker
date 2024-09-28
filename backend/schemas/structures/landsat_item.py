from datetime import datetime

from pydantic import BaseModel

from backend.schemas.structures.cloud_coverage_ratio import CloudCoverageRatio
from backend.schemas.structures.polygon import Polygon
from backend.schemas.structures.wrs_coordinates import WrsCoordinates


class LandsatItem(BaseModel):
    id: str
    scene_id: str
    datetime: datetime
    eo_cloud_cover: CloudCoverageRatio
    wrs_coordinates: WrsCoordinates
    rendered_preview: str
    polygon: Polygon
