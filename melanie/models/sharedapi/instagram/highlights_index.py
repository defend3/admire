# generated by datamodel-codegen:
#   timestamp: 2023-01-08T11:08:15+00:00


from __future__ import annotations

from typing import Any

from melanie import BaseModel


class PurpleNode(BaseModel):
    id: str | None
    blocked_by_viewer: bool | None
    restricted_by_viewer: bool | None
    followed_by_viewer: bool | None
    follows_viewer: bool | None
    full_name: str | None
    has_blocked_viewer: bool | None
    has_requested_viewer: bool | None
    is_private: bool | None
    is_verified: bool | None
    profile_pic_url: str | None
    requested_by_viewer: bool | None
    username: str | None


class CoverMedia(BaseModel):
    thumbnail_src: str | None


class CoverMediaCroppedThumbnail(BaseModel):
    url: str | None


class Owner(BaseModel):
    id: str | None
    profile_pic_url: str | None
    username: str | None


class Reel(BaseModel):
    id: str | None
    expiring_at: int | None
    has_pride_media: bool | None
    latest_reel_media: int | None
    seen: Any | None
    user: Owner | None
    owner: Owner | None


class Viewer(BaseModel):
    pass


class EdgeChainingEdge(BaseModel):
    node: PurpleNode | None


class FluffyNode(BaseModel):
    id: str | None
    cover_media: CoverMedia | None
    cover_media_cropped_thumbnail: CoverMediaCroppedThumbnail | None
    owner: Owner | None
    title: str | None


class EdgeChaining(BaseModel):
    edges: list[EdgeChainingEdge] | None


class EdgeHighlightReelsEdge(BaseModel):
    node: FluffyNode | None


class EdgeHighlightReels(BaseModel):
    edges: list[EdgeHighlightReelsEdge] | None


class User(BaseModel):
    is_live: bool | None
    reel: Reel | None
    edge_chaining: EdgeChaining | None
    edge_highlight_reels: EdgeHighlightReels | None


class Data(BaseModel):
    viewer: Viewer | None
    user: User | None


class InstagramHighlightGraphQueryRaw(BaseModel):
    data: Data | None
    status: str | None


class HighlightItem(BaseModel):
    preview_img: str | None
    title: str | None
    id: str


class InstagramHighlightIndexResponse(BaseModel):
    count: int = 0
    highlights: list[HighlightItem] = []
