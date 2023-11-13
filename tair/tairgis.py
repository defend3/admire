from typing import Dict, List, Optional

from tair.typing import CommandsProtocol, EncodableT, FieldT, KeyT, ResponseT


class TairGisSearchRadius:
    def __init__(self, longitude: float, latitude: float, distance: float, unit: str) -> None:
        self.longitude = longitude
        self.latitude = latitude
        self.distance = distance
        self.unit = unit

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TairGisSearchRadius):
            return False
        return self.longitude == other.longitude and self.latitude == other.latitude and self.distance == other.distance and self.unit == other.unit

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return "{" + f"longitude: {self.longitude}, " + f"latitude: {self.latitude}, " + f"distance: {self.distance}, " + f"unit: {self.unit}" + "}"


class TairGisSearchMember:
    def __init__(self, field: FieldT, distance: float, unit) -> None:
        self.field = field
        self.distance = distance
        self.unit = unit

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TairGisSearchMember):
            return False
        return self.field == other.field and self.distance == other.distance and self.unit == other.unit

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return "{" + f"field: {self.field}, " + f"distance: {self.distance}, " + f"unit: {self.unit}" + "}"


class TairGisCommands(CommandsProtocol):
    def gis_add(self, area: KeyT, mapping: Dict[KeyT, str]) -> ResponseT:
        pieces: List[EncodableT] = [area]

        for name, wkt in mapping.items():
            pieces.extend((name, wkt))
        return self.execute_command("GIS.ADD", *pieces)

    def gis_get(self, area: KeyT, polygon_name: EncodableT) -> ResponseT:
        return self.execute_command("GIS.GET", area, polygon_name)

    def gis_getall(self, area: KeyT, withoutwkts: bool = False) -> ResponseT:
        if withoutwkts:
            return self.execute_command("GIS.GETALL", area, "WITHOUTWKT")
        return self.execute_command("GIS.GETALL", area)

    def gis_contains(self, area: KeyT, polygon_wkt: EncodableT, withoutwkts: bool = False) -> ResponseT:
        if withoutwkts:
            return self.execute_command("GIS.CONTAINS", area, polygon_wkt, "WITHOUTWKT")
        return self.execute_command("GIS.CONTAINS", area, polygon_wkt)

    def gis_within(self, area: KeyT, polygon_wkt: EncodableT, withoutwkts: bool = False) -> ResponseT:
        if withoutwkts:
            return self.execute_command("GIS.WITHIN", area, polygon_wkt, "WITHOUTWKT")
        return self.execute_command("GIS.WITHIN", area, polygon_wkt)

    def gis_intersects(self, area: KeyT, polygon_wkt: EncodableT, withoutwkts: bool = False) -> ResponseT:
        if withoutwkts:
            return self.execute_command("GIS.INTERSECTS", area, polygon_wkt, "WITHOUTWKT")
        return self.execute_command("GIS.INTERSECTS", area, polygon_wkt)

    def gis_search(
        self,
        area: KeyT,
        radius: Optional[TairGisSearchRadius] = None,
        member: Optional[TairGisSearchMember] = None,
        geom: Optional[EncodableT] = None,
        count: Optional[int] = None,
        asc: bool = True,
        desc: bool = False,
        withdist: bool = False,
        withoutwkts: bool = False,
    ) -> ResponseT:
        pieces: List[EncodableT] = [area]

        if radius:
            pieces.extend(("RADIUS", radius.longitude, radius.latitude, radius.distance, radius.unit))
        if member:
            pieces.extend(("MEMBER", member.field, member.distance, member.unit))
        if geom:
            pieces.append("GEOM")
            pieces.append(geom)
        if count:
            pieces.append("COUNT")
            pieces.append(count)
        if asc:
            pieces.append("ASC")
        if desc:
            pieces.append("DESC")
        if withdist:
            pieces.append("WITHDIST")
        if withoutwkts:
            pieces.append("WITHOUTWKT")

        return self.execute_command("GIS.SEARCH", *pieces)

    def gis_del(self, area: KeyT, polygen_name) -> ResponseT:
        return self.execute_command("GIS.DEL", area, polygen_name)
