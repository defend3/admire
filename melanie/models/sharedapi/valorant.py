# generated by datamodel-codegen:
#   timestamp: 2023-01-18T10:04:05+00:00


from __future__ import annotations

from datetime import datetime  # noqa
from typing import Annotated, Any

from melanie import BaseModel, Field

from .valorant2 import MMRData, UserinfoData  # noqa


class ActivePlayerCounts(BaseModel):
    valorant: int | None


class Valorant(BaseModel):
    platform_id: str | None


class Attributes(BaseModel):
    key: str | None
    playlist: str | None
    map_key: str | None
    agent_key: str | None
    category_key: str | None
    season_id: str | None


class Ability1(BaseModel):
    name: str | None
    image_url: str | None


class Ability1CastsMetadata(BaseModel):
    icon_url: str | None
    tier_name: str | None
    act_id: str | None
    act_name: str | None


class Ability1Kills(BaseModel):
    display_name: str | None
    display_value: Any | None
    display_type: str | None


class RankMetadata(BaseModel):
    icon_url: str | None
    tier_name: str | None


class StandardProfileMetadata(BaseModel):
    active_shard: str | None
    schema_: Annotated[str | None, Field(alias="schema")]
    privacy: str | None
    default_playlist: str | None
    default_season: str | None
    premier_roster_id: str | None
    account_level: int | None


class PlatformInfo(BaseModel):
    platform_slug: str | None
    platform_user_id: str | None
    platform_user_handle: str | None
    platform_user_identifier: str | None
    avatar_url: str | None


class Passive(BaseModel):
    name: str | None


class TrnPerformanceScoreMetadata(BaseModel):
    stats: list[str] | None


class SocialAccount(BaseModel):
    platform_slug: str | None
    platform_user_handle: str | None
    platform_user_identifier: str | None


class AdUnits(BaseModel):
    desktop__header: str | None
    desktop__content__atf: str | None
    desktop__content__btf: str | None
    desktop__sidebar__a: str | None
    desktop__sidebar__b: str | None
    desktop__footer: str | None
    desktop__footer__rectangle: str | None
    mobile__header: str | None
    mobile__content__atf: str | None
    mobile__content__btf: str | None
    mobile__footer__rectangle: str | None
    desktop__content_300x600: str | None
    desktop__content_160x600: str | None
    desktop__content_728x90: str | None


class Endpoints(BaseModel):
    ads: str | None


class Widgets(BaseModel):
    components: list[str] | None


class Images(BaseModel):
    home_hero_background: str | None
    default_avatar_url: str | None
    default_hero_url: str | None
    not_found_background: str | None
    premium_hero_background: str | None
    boxart_url: str | None


class ItemItem(BaseModel):
    label: str | None
    to: str | None
    img: str | None


class Mobile(BaseModel):
    app_store_ppid: str | None


class Social(BaseModel):
    twitter: str | None


class CurrentTitleSettingsTheme(BaseModel):
    border_radius: str | None
    color_accent: str | None
    color_action: str | None
    color_gradient_high1: str | None
    color_gradient_high2: str | None
    color_gradient_low1: str | None
    color_gradient_low2: str | None
    color_background: str | None
    color_surface1: str | None
    color_surface3: str | None
    color_surface2: str | None
    color_main_nav_background: str | None
    color_game_bar_background: str | None
    color_text_primary: str | None
    color_text_secondary: str | None
    graph_color_palette: list[str] | None


class PlatformTheme(BaseModel):
    primary_color: str | None


class Publisher(BaseModel):
    name: str | None
    notice: str | None


class Option(BaseModel):
    label: str | None
    value: str | None
    default: bool | None
    icon: str | None


class Hint(BaseModel):
    key: str | None
    title: str | None
    body: str | None


class Category(BaseModel):
    key: str | None
    label: str | None
    tags: list[str] | None


class PopulationCharts(BaseModel):
    use_chunked_mau: bool | None


class Search(BaseModel):
    search_additional_results: bool | None
    autocomplete: bool | None
    placeholder: str | None


class Subscriptions(BaseModel):
    enabled: bool | None


class Ability(BaseModel):
    slot: str | None
    display_name: str | None
    description: str | None
    display_icon: str | None


class Role(BaseModel):
    name: str | None
    icon_url: str | None


class Map(BaseModel):
    slug: str | None
    name: str | None
    coordinates: str | None
    image_url: str | None
    uuid: str | None


class Playlist(BaseModel):
    value: str | None
    label: str | None


class Season(BaseModel):
    id: str | None
    name: str | None
    short_name: str | None
    start_time: datetime | None
    end_time: datetime | None
    seasons: list[Season] | None


class Wrapper(BaseModel):
    is_loaded: bool | None


class ValorantDataRawLfg(BaseModel):
    active_player_counts: ActivePlayerCounts | None


class Options(BaseModel):
    valorant: Valorant | None


class PurpleAbilities(BaseModel):
    ability1: Ability1 | None
    ability2: Ability1 | None
    grenade: Ability1 | None
    ultimate: Ability1 | None
    passive: Ability1 | None


class Ability1Casts(BaseModel):
    display_name: str | None
    display_category: str | None
    category: str | None
    value: float | None
    display_value: Any | None
    display_type: str | None
    percentile: float | None
    description: str | None
    metadata: Ability1CastsMetadata | None


class Rank(BaseModel):
    rank: int | None
    display_name: str | None
    category: str | None
    metadata: RankMetadata | None
    value: int | None
    display_value: Any | None
    display_type: str | None


class FluffyAbilities(BaseModel):
    ability2: Ability1 | None
    grenade: Ability1 | None
    ability1: Ability1 | None
    ultimate: Ability1 | None
    passive: Passive | None


class TrnPerformanceScore(BaseModel):
    display_name: str | None
    metadata: TrnPerformanceScoreMetadata | None
    value: int | None
    display_value: Any | None
    display_type: str | None


class UserInfo(BaseModel):
    user_id: int | None
    country_code: str | None
    social_accounts: list[SocialAccount] | None
    pageviews: int | None


class Home(BaseModel):
    widgets: Widgets | None


class NavigationItem(BaseModel):
    label: str | None
    description: str | None
    to: str | None
    items: list[ItemItem] | None
    is_new: bool | None
    key: str | None
    collapse: bool | None


class Promos(BaseModel):
    mobile: Mobile | None


class Platform(BaseModel):
    slug: str | None
    name: str | None
    has_sign_in: bool | None
    theme: PlatformTheme | None


class Filter(BaseModel):
    key: str | None
    placeholder: str | None
    description: str | None
    is_available_in_lfg_form: bool | None
    is_required_in_lfg_form: bool | None
    options: list[Option] | None
    is_activity_filter: bool | None
    is_multiple_selection: bool | None


class News(BaseModel):
    enabled: bool | None
    categories: list[Category] | None


class Agent(BaseModel):
    uuid: str | None
    slug: str | None
    name: str | None
    description: str | None
    color: str | None
    image_url: str | None
    thumb_image_url: str | None
    abilities: list[Ability] | None
    role: Role | None


class RiotRgea(BaseModel):
    options: Options | None


class PurpleMetadata(BaseModel):
    name: str | None
    image_url: str | None
    role: str | None
    color: str | None
    abilities: PurpleAbilities | None
    schema_: Annotated[str | None, Field(alias="schema")]
    category: str | None


class PurpleStats(BaseModel):
    matches_played: Ability1Casts | None
    matches_won: Ability1Casts | None
    matches_lost: Ability1Casts | None
    matches_tied: Ability1Casts | None
    matches_win_pct: Ability1Casts | None
    time_played: Ability1Casts | None
    score_per_round: Ability1Casts | None
    kills: Ability1Casts | None
    deaths: Ability1Casts | None
    assists: Ability1Casts | None
    k_d_ratio: Ability1Casts | None
    k_ad_ratio: Ability1Casts | None
    damage_delta: Ability1Casts | None
    damage_delta_per_round: Ability1Casts | None
    damage_per_round: Ability1Casts | None
    k_ast: Ability1Casts | None
    matches_disconnected: Ability1Casts | None
    matches_duration: Ability1Casts | None
    rounds_played: Ability1Casts | None
    rounds_won: Ability1Casts | None
    rounds_lost: Ability1Casts | None
    rounds_win_pct: Ability1Casts | None
    rounds_duration: Ability1Casts | None
    score: Ability1Casts | None
    score_per_match: Ability1Casts | None
    kills_per_round: Ability1Casts | None
    kills_per_match: Ability1Casts | None
    deaths_per_round: Ability1Casts | None
    deaths_per_match: Ability1Casts | None
    assists_per_round: Ability1Casts | None
    assists_per_match: Ability1Casts | None
    k_da_ratio: Ability1Casts | None
    damage: Ability1Casts | None
    damage_per_match: Ability1Casts | None
    damage_per_minute: Ability1Casts | None
    damage_received: Ability1Casts | None
    headshots: Ability1Casts | None
    headshots_per_round: Ability1Casts | None
    headshots_percentage: Ability1Casts | None
    grenade_casts: Ability1Casts | None
    grenade_casts_per_round: Ability1Casts | None
    grenade_casts_per_match: Ability1Casts | None
    ability1_casts: Ability1Casts | None
    ability1_casts_per_round: Ability1Casts | None
    ability1_casts_per_match: Ability1Casts | None
    ability2_casts: Ability1Casts | None
    ability2_casts_per_round: Ability1Casts | None
    ability2_casts_per_match: Ability1Casts | None
    ultimate_casts: Ability1Casts | None
    ultimate_casts_per_round: Ability1Casts | None
    ultimate_casts_per_match: Ability1Casts | None
    dealt_headshots: Ability1Casts | None
    dealt_bodyshots: Ability1Casts | None
    dealt_legshots: Ability1Casts | None
    received_headshots: Ability1Casts | None
    received_bodyshots: Ability1Casts | None
    received_legshots: Ability1Casts | None
    econ_rating: Ability1Casts | None
    econ_rating_per_match: Ability1Casts | None
    econ_rating_per_round: Ability1Casts | None
    suicides: Ability1Casts | None
    first_bloods: Ability1Casts | None
    first_bloods_per_round: Ability1Casts | None
    first_bloods_per_match: Ability1Casts | None
    first_deaths: Ability1Casts | None
    first_deaths_per_round: Ability1Casts | None
    last_deaths: Ability1Casts | None
    survived: Ability1Casts | None
    traded: Ability1Casts | None
    most_kills_in_match: Ability1Casts | None
    flawless: Ability1Casts | None
    thrifty: Ability1Casts | None
    aces: Ability1Casts | None
    team_aces: Ability1Casts | None
    clutches: Ability1Casts | None
    clutches_percentage: Ability1Casts | None
    clutches_lost: Ability1Casts | None
    clutches1v1: Ability1Casts | None
    clutches1v2: Ability1Casts | None
    clutches1v3: Ability1Casts | None
    clutches1v4: Ability1Casts | None
    clutches1v5: Ability1Casts | None
    clutches_lost1v1: Ability1Casts | None
    clutches_lost1v2: Ability1Casts | None
    clutches_lost1v3: Ability1Casts | None
    clutches_lost1v4: Ability1Casts | None
    clutches_lost1v5: Ability1Casts | None
    kills1_k: Ability1Casts | None
    kills2_k: Ability1Casts | None
    kills3_k: Ability1Casts | None
    kills4_k: Ability1Casts | None
    kills5_k: Ability1Casts | None
    kills6_k: Ability1Casts | None
    esr: Ability1Casts | None
    plants: Ability1Casts | None
    plants_per_match: Ability1Casts | None
    plants_per_round: Ability1Casts | None
    attack_kills: Ability1Casts | None
    attack_kills_per_round: Ability1Casts | None
    attack_deaths: Ability1Casts | None
    attack_kd_ratio: Ability1Casts | None
    attack_assists: Ability1Casts | None
    attack_assists_per_round: Ability1Casts | None
    attack_rounds_won: Ability1Casts | None
    attack_rounds_lost: Ability1Casts | None
    attack_rounds_played: Ability1Casts | None
    attack_rounds_win_pct: Ability1Casts | None
    attack_score: Ability1Casts | None
    attack_score_per_round: Ability1Casts | None
    attack_damage: Ability1Casts | None
    attack_damage_per_round: Ability1Casts | None
    attack_headshots: Ability1Casts | None
    attack_traded: Ability1Casts | None
    attack_survived: Ability1Casts | None
    attack_first_bloods: Ability1Casts | None
    attack_first_bloods_per_round: Ability1Casts | None
    attack_first_deaths: Ability1Casts | None
    attack_first_deaths_per_round: Ability1Casts | None
    attack_kast: Ability1Casts | None
    defuses: Ability1Casts | None
    defuses_per_match: Ability1Casts | None
    defuses_per_round: Ability1Casts | None
    defense_kills: Ability1Casts | None
    defense_kills_per_round: Ability1Casts | None
    defense_deaths: Ability1Casts | None
    defense_kd_ratio: Ability1Casts | None
    defense_assists: Ability1Casts | None
    defense_assists_per_round: Ability1Casts | None
    defense_rounds_won: Ability1Casts | None
    defense_rounds_lost: Ability1Casts | None
    defense_rounds_played: Ability1Casts | None
    defense_rounds_win_pct: Ability1Casts | None
    defense_score: Ability1Casts | None
    defense_score_per_round: Ability1Casts | None
    defense_damage: Ability1Casts | None
    defense_damage_per_round: Ability1Casts | None
    defense_headshots: Ability1Casts | None
    defense_traded: Ability1Casts | None
    defense_survived: Ability1Casts | None
    defense_first_bloods: Ability1Casts | None
    defense_first_bloods_per_round: Ability1Casts | None
    defense_first_deaths: Ability1Casts | None
    defense_first_deaths_per_round: Ability1Casts | None
    defense_kast: Ability1Casts | None
    ability1_kills: Ability1Kills | None
    ability1_kills_per_match: Ability1Kills | None
    ability2_kills: Ability1Kills | None
    ability2_kills_per_match: Ability1Kills | None
    grenade_kills: Ability1Kills | None
    grenade_kills_per_match: Ability1Kills | None
    primary_kills: Ability1Kills | None
    primary_kills_per_match: Ability1Kills | None
    ultimate_kills: Ability1Kills | None
    ultimate_kills_per_match: Ability1Kills | None
    secondary_kills: Ability1Casts | None
    secondary_kills_per_round: Ability1Casts | None
    secondary_kills_per_match: Ability1Casts | None
    kill_distance: Ability1Casts | None
    avg_kill_distance: Ability1Casts | None
    longest_kill_distance: Ability1Casts | None
    rank: Rank | None
    peak_rank: Ability1Casts | None


class FluffyMetadata(BaseModel):
    name: str | None
    playlist_name: str | None
    start_time: datetime | None
    end_time: datetime | None
    schema_: Annotated[str | None, Field(alias="schema")]
    image_url: str | None
    category: str | None
    color: str | None
    role: str | None
    abilities: FluffyAbilities | None


class FluffyStats(BaseModel):
    matches_played: Ability1Casts | None
    matches_won: Ability1Casts | None
    matches_lost: Ability1Casts | None
    matches_tied: Ability1Casts | None
    matches_win_pct: Ability1Casts | None
    matches_disconnected: Ability1Casts | None
    matches_duration: Ability1Casts | None
    time_played: Ability1Casts | None
    rounds_played: Ability1Casts | None
    rounds_won: Ability1Casts | None
    rounds_lost: Ability1Casts | None
    rounds_win_pct: Ability1Casts | None
    rounds_duration: Ability1Casts | None
    score: Ability1Casts | None
    score_per_match: Ability1Casts | None
    score_per_round: Ability1Casts | None
    kills: Ability1Casts | None
    kills_per_round: Ability1Casts | None
    kills_per_match: Ability1Casts | None
    deaths: Ability1Casts | None
    deaths_per_round: Ability1Casts | None
    deaths_per_match: Ability1Casts | None
    assists: Ability1Casts | None
    assists_per_round: Ability1Casts | None
    assists_per_match: Ability1Casts | None
    k_d_ratio: Ability1Casts | None
    k_da_ratio: Ability1Casts | None
    k_ad_ratio: Ability1Casts | None
    damage: Ability1Casts | None
    damage_delta: Ability1Casts | None
    damage_delta_per_round: Ability1Casts | None
    damage_per_round: Ability1Casts | None
    damage_per_match: Ability1Casts | None
    damage_per_minute: Ability1Casts | None
    damage_received: Ability1Casts | None
    headshots: Ability1Casts | None
    headshots_per_round: Ability1Casts | None
    headshots_percentage: Ability1Casts | None
    grenade_casts: Ability1Casts | None
    grenade_casts_per_round: Ability1Casts | None
    grenade_casts_per_match: Ability1Casts | None
    ability1_casts: Ability1Casts | None
    ability1_casts_per_round: Ability1Casts | None
    ability1_casts_per_match: Ability1Casts | None
    ability2_casts: Ability1Casts | None
    ability2_casts_per_round: Ability1Casts | None
    ability2_casts_per_match: Ability1Casts | None
    ultimate_casts: Ability1Casts | None
    ultimate_casts_per_round: Ability1Casts | None
    ultimate_casts_per_match: Ability1Casts | None
    dealt_headshots: Ability1Casts | None
    dealt_bodyshots: Ability1Casts | None
    dealt_legshots: Ability1Casts | None
    received_headshots: Ability1Casts | None
    received_bodyshots: Ability1Casts | None
    received_legshots: Ability1Casts | None
    econ_rating: Ability1Casts | None
    econ_rating_per_match: Ability1Casts | None
    econ_rating_per_round: Ability1Casts | None
    suicides: Ability1Casts | None
    first_bloods: Ability1Casts | None
    first_bloods_per_round: Ability1Casts | None
    first_bloods_per_match: Ability1Casts | None
    first_deaths: Ability1Casts | None
    first_deaths_per_round: Ability1Casts | None
    last_deaths: Ability1Casts | None
    survived: Ability1Casts | None
    traded: Ability1Casts | None
    k_ast: Ability1Casts | None
    most_kills_in_match: Ability1Casts | None
    flawless: Ability1Casts | None
    thrifty: Ability1Casts | None
    aces: Ability1Casts | None
    team_aces: Ability1Casts | None
    clutches: Ability1Casts | None
    clutches_percentage: Ability1Casts | None
    clutches_lost: Ability1Casts | None
    clutches1v1: Ability1Casts | None
    clutches1v2: Ability1Casts | None
    clutches1v3: Ability1Casts | None
    clutches1v4: Ability1Casts | None
    clutches1v5: Ability1Casts | None
    clutches_lost1v1: Ability1Casts | None
    clutches_lost1v2: Ability1Casts | None
    clutches_lost1v3: Ability1Casts | None
    clutches_lost1v4: Ability1Casts | None
    clutches_lost1v5: Ability1Casts | None
    kills1_k: Ability1Casts | None
    kills2_k: Ability1Casts | None
    kills3_k: Ability1Casts | None
    kills4_k: Ability1Casts | None
    kills5_k: Ability1Casts | None
    kills6_k: Ability1Casts | None
    esr: Ability1Casts | None
    plants: Ability1Casts | None
    plants_per_match: Ability1Casts | None
    plants_per_round: Ability1Casts | None
    attack_kills: Ability1Casts | None
    attack_kills_per_round: Ability1Casts | None
    attack_deaths: Ability1Casts | None
    attack_kd_ratio: Ability1Casts | None
    attack_assists: Ability1Casts | None
    attack_assists_per_round: Ability1Casts | None
    attack_rounds_won: Ability1Casts | None
    attack_rounds_lost: Ability1Casts | None
    attack_rounds_played: Ability1Casts | None
    attack_rounds_win_pct: Ability1Casts | None
    attack_score: Ability1Casts | None
    attack_score_per_round: Ability1Casts | None
    attack_damage: Ability1Casts | None
    attack_damage_per_round: Ability1Casts | None
    attack_headshots: Ability1Casts | None
    attack_traded: Ability1Casts | None
    attack_survived: Ability1Casts | None
    attack_first_bloods: Ability1Casts | None
    attack_first_bloods_per_round: Ability1Casts | None
    attack_first_deaths: Ability1Casts | None
    attack_first_deaths_per_round: Ability1Casts | None
    attack_kast: Ability1Casts | None
    defuses: Ability1Casts | None
    defuses_per_match: Ability1Casts | None
    defuses_per_round: Ability1Casts | None
    defense_kills: Ability1Casts | None
    defense_kills_per_round: Ability1Casts | None
    defense_deaths: Ability1Casts | None
    defense_kd_ratio: Ability1Casts | None
    defense_assists: Ability1Casts | None
    defense_assists_per_round: Ability1Casts | None
    defense_rounds_won: Ability1Casts | None
    defense_rounds_lost: Ability1Casts | None
    defense_rounds_played: Ability1Casts | None
    defense_rounds_win_pct: Ability1Casts | None
    defense_score: Ability1Casts | None
    defense_score_per_round: Ability1Casts | None
    defense_damage: Ability1Casts | None
    defense_damage_per_round: Ability1Casts | None
    defense_headshots: Ability1Casts | None
    defense_traded: Ability1Casts | None
    defense_survived: Ability1Casts | None
    defense_first_bloods: Ability1Casts | None
    defense_first_bloods_per_round: Ability1Casts | None
    defense_first_deaths: Ability1Casts | None
    defense_first_deaths_per_round: Ability1Casts | None
    defense_kast: Ability1Casts | None
    rank: Rank | None
    trn_performance_score: TrnPerformanceScore | None
    peak_rank: Ability1Casts | None
    secondary_kills: Ability1Casts | None
    secondary_kills_per_round: Ability1Casts | None
    secondary_kills_per_match: Ability1Casts | None
    kill_distance: Ability1Casts | None
    avg_kill_distance: Ability1Casts | None
    longest_kill_distance: Ability1Casts | None
    ability1_kills: Ability1Kills | None
    ability1_kills_per_match: Ability1Kills | None
    ability2_kills: Ability1Kills | None
    ability2_kills_per_match: Ability1Kills | None
    grenade_kills: Ability1Kills | None
    grenade_kills_per_match: Ability1Kills | None
    primary_kills: Ability1Kills | None
    primary_kills_per_match: Ability1Kills | None
    ultimate_kills: Ability1Kills | None
    ultimate_kills_per_match: Ability1Kills | None


class Navigation(BaseModel):
    items: list[NavigationItem] | None


class Title(BaseModel):
    name: str | None
    seo_name: str | None
    slug: str | None
    publisher: Publisher | None
    platforms: list[Platform] | None


class UILfg(BaseModel):
    post_duration_hours: int | None
    filters: list[Filter] | None
    hint: Hint | None


class TypeLists(BaseModel):
    playlists: list[Playlist] | None
    seasons: list[Season] | None
    agents: list[Agent] | None
    maps: list[Map] | None


class StatsSegment(BaseModel):
    type: str | None
    attributes: Attributes | None
    metadata: PurpleMetadata | None
    expiry_date: datetime | None
    stats: PurpleStats | None
    field_key: Annotated[str | None, Field(alias="_key")]
    field_fetch_key: Annotated[str | None, Field(alias="_fetch_key")]
    field_profile_key: Annotated[str | None, Field(alias="_profile_key")]


class StandardProfileSegment(BaseModel):
    type: str | None
    attributes: Attributes | None
    metadata: FluffyMetadata | None
    expiry_date: datetime | None
    stats: FluffyStats | None


class UI(BaseModel):
    search: Search | None
    subscriptions: Subscriptions | None
    news: News | None
    population_charts: PopulationCharts | None
    lfg: UILfg | None


class ValorantDB(BaseModel):
    type_lists: TypeLists | None


class StandardProfile(BaseModel):
    platform_info: PlatformInfo | None
    user_info: UserInfo | None
    metadata: StandardProfileMetadata | None
    segments: list[StandardProfileSegment] | None
    expiry_date: datetime | None
    field_key: Annotated[str | None, Field(alias="_key")]


class CurrentTitleSettings(BaseModel):
    site_name: str | None
    site_description: str | None
    site_support_domain: str | None
    home: Home | None
    ui: UI | None
    title: Title | None
    endpoints: Endpoints | None
    google_analytics: list[str] | None
    google_site_verification: str | None
    riot_rgea_property_id: str | None
    images: Images | None
    theme: CurrentTitleSettingsTheme | None
    navigation: Navigation | None
    ad_units: AdUnits | None
    social: Social | None
    promos: Promos | None
    base_uri: str | None


class ValorantDataRawStats(BaseModel):
    standard_profiles: list[StandardProfile] | None
    segments: list[StatsSegment] | None


class Titles(BaseModel):
    current_title_slug: str | None
    current_title_settings: CurrentTitleSettings | None


class ValorantDataRaw(BaseModel):
    titles: Titles | None
    riot_rgea: RiotRgea | None
    lfg: ValorantDataRawLfg | None
    stats: ValorantDataRawStats | None
    valorant_db: ValorantDB | None
    wrapper: Wrapper | None


class Card(BaseModel):
    small: str | None
    large: str | None
    wide: str | None
    id: str | None


class Data(BaseModel):
    puuid: str | None
    region: str | None
    account_level: int | None
    name: str | None
    tag: str | None
    card: Card | None
    last_update: str | None
    last_update_raw: int | None


class ValorantAPI2Raw(BaseModel):
    status: int | None
    data: Data | None


class ValorantProfileResponse(BaseModel):
    account_level: int | None
    avatar_url: str | None
    card: Card | None
    current_rating: str | None
    damage_round_ratio: float | None
    deaths: int | None
    headshot_percent: float | None
    info: UserinfoData | None
    kd_ratio: float | None
    kills: int | None
    last_update: int | None
    lost: int | None
    matches_played: int | None
    mmr: MMRData | None
    name: str | None
    peak_rating_act: str | None
    peak_rating: str | None
    puuid: str | None
    region: str | None
    tag: str | None
    win_percent: float | None
    wins: int | None


Season.update_forward_refs()
