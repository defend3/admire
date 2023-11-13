# generated by datamodel-codegen:
#   timestamp: 2022-12-06T00:28:32+00:00


from __future__ import annotations

from datetime import date  # noqa
from typing import Any

from melanie import BaseModel, Field


class LivingstoneSouthernWhiteFacedOwl(BaseModel):
    uri: str | None
    url_list: list[str] | None
    width: int | None
    height: int | None
    data_size: int | None


class PlayAddr(BaseModel):
    uri: str | None
    url_list: list[str] | None
    width: int | None
    height: int | None
    url_key: str | None
    data_size: int | None
    file_hash: str | None


class BitRate(BaseModel):
    gear_name: str | None
    quality_type: int | None
    bit_rate: int | None
    play_addr: PlayAddr | None
    is_bytevc1: int | None
    dub_infos: Any | None
    hdr_type: str | None = Field(None, alias="HDR_type")
    hdr_bit: str | None = Field(None, alias="HDR_bit")


class HammerfestPonies(BaseModel):
    height: int | None
    uri: str | None
    url_list: list[str] | None
    width: int | None


class MatchedFriend(BaseModel):
    video_items: Any | None


class AuthorShareInfo(BaseModel):
    now_invitation_card_image_urls: Any | None
    share_qrcode_url: HammerfestPonies | None


class ChaListShareInfo(BaseModel):
    bool_persist: int | None
    now_invitation_card_image_urls: Any | None
    share_desc: str | None
    share_desc_info: str | None
    share_title: str | None
    share_url: str | None
    share_weibo_desc: str | None


class Image(BaseModel):
    bitrate_images: Any | None
    display_image: HammerfestPonies | None
    owner_watermark_image: HammerfestPonies | None
    thumbnail: HammerfestPonies | None
    user_watermark_image: HammerfestPonies | None


class Music(BaseModel):
    artists: Any | None
    author: str | None
    author_deleted: bool | None
    author_position: Any | None
    avatar_large: HammerfestPonies | None
    avatar_medium: HammerfestPonies | None
    avatar_thumb: HammerfestPonies | None
    binded_challenge_id: int | None
    collect_stat: int | None
    cover_hd: HammerfestPonies | None
    cover_large: HammerfestPonies | None
    cover_medium: HammerfestPonies | None
    cover_thumb: HammerfestPonies | None
    duration: int | None
    end_time: int | None
    external_song_info: list | None
    extra: str | None
    id: int | None
    id_str: str | None
    is_author_artist: bool | None
    is_commerce_music: bool | None
    is_del_video: bool | None
    is_original: bool | None
    is_original_sound: bool | None
    is_pgc: bool | None
    is_restricted: bool | None
    is_video_self_see: bool | None
    lyric_short_position: Any | None
    mid: str | None
    multi_bit_rate_play_info: Any | None
    mute_share: bool | None
    owner_handle: str | None
    owner_id: str | None
    owner_nickname: str | None
    play_url: HammerfestPonies | None
    position: Any | None
    prevent_download: bool | None
    prevent_item_download_status: int | None
    preview_end_time: int | None
    preview_start_time: int | None
    redirect: bool | None
    search_highlight: Any | None
    source_platform: int | None
    start_time: int | None
    status: int | None
    strong_beat_url: HammerfestPonies | None
    tag_list: Any | None
    title: str | None
    user_count: int | None


class RiskInfos(BaseModel):
    risk_sink: bool | None
    type: int | None
    vote: bool | None
    warn: bool | None


class Statistics(BaseModel):
    aweme_id: str | None
    collect_count: int | None
    comment_count: int | None
    digg_count: int | None
    download_count: int | None
    forward_count: int | None
    lose_comment_count: int | None
    lose_count: int | None
    play_count: int | None
    share_count: int | None
    whatsapp_share_count: int | None


class Status(BaseModel):
    allow_comment: bool | None
    allow_share: bool | None
    aweme_id: str | None
    download_status: int | None
    in_reviewing: bool | None
    is_delete: bool | None
    is_private: bool | None
    is_prohibited: bool | None
    private_status: int | None
    reviewed: int | None
    self_see: bool | None
    with_goods: bool | None


class TextExtra(BaseModel):
    end: int | None
    hashtag_id: str | None
    hashtag_name: str | None
    is_commerce: bool | None
    start: int | None
    type: int | None


class CaptionInfo(BaseModel):
    lang: str | None
    language_id: int | None
    url: str | None
    expire: int | None
    caption_format: str | None
    complaint_id: int | None
    is_auto_generated: bool | None
    sub_id: int | None
    sub_version: int | None
    cla_subtitle_id: int | None
    translator_id: int | None
    language_code: str | None


class OriginalLanguageInfo(BaseModel):
    lang: str | None
    language_id: int | None
    language_code: str | None
    can_translate_realtime: bool | None


class ClaInfo(BaseModel):
    has_original_audio: int | None
    enable_auto_caption: int | None
    original_language_info: OriginalLanguageInfo | None
    caption_infos: list[CaptionInfo] | None
    vertical_positions: Any | None
    hide_original_caption: bool | None


class Video(BaseModel):
    play_addr: PlayAddr | None
    cover: LivingstoneSouthernWhiteFacedOwl | None
    height: int | None
    width: int | None
    dynamic_cover: LivingstoneSouthernWhiteFacedOwl | None
    origin_cover: LivingstoneSouthernWhiteFacedOwl | None
    ratio: str | None
    download_addr: LivingstoneSouthernWhiteFacedOwl | None
    has_watermark: bool | None
    bit_rate: list[BitRate] | None
    duration: int | None
    play_addr_h264: PlayAddr | None
    cdn_url_expired: int | None
    need_set_token: bool | None
    misc_download_addrs: str | None
    tags: Any | None
    big_thumbs: Any | None
    play_addr_bytevc1: PlayAddr | None
    is_bytevc1: int | None
    meta: str | None
    cla_info: ClaInfo | None
    source_hdr_type: int | None = Field(None, alias="source_HDR_type")


class VideoControl(BaseModel):
    allow_download: bool | None
    allow_duet: bool | None
    allow_dynamic_wallpaper: bool | None
    allow_music: bool | None
    allow_react: bool | None
    allow_stitch: bool | None
    draft_progress_bar: int | None
    prevent_download_type: int | None
    share_type: int | None
    show_progress_bar: int | None
    timer_status: int | None


class Format(BaseModel):
    acodec: str | None
    audio_ext: str | None
    ext: str | None
    filesize: Any | None
    format_id: str | None
    format_note: str | None
    height: int | None
    protocol: str | None
    source_preference: int | None
    url: str | None
    vcodec: str | None
    video_ext: str | None
    width: int | None


class Subtitles(BaseModel):
    pass


class Thumbnail(BaseModel):
    id: str | None
    url: str | None


class Author(BaseModel):
    accept_private_policy: bool | None
    account_labels: Any | None
    ad_cover_url: Any | None
    advance_feature_item_order: Any | None
    advanced_feature_info: Any | None
    apple_account: int | None
    authority_status: int | None
    avatar_168x168: HammerfestPonies | None
    avatar_300x300: HammerfestPonies | None
    avatar_larger: HammerfestPonies | None
    avatar_medium: HammerfestPonies | None
    avatar_thumb: HammerfestPonies | None
    avatar_uri: str | None
    aweme_count: int | None
    birthday: date | None
    bold_fields: Any | None
    can_message_follow_status_list: Any | None
    can_set_geofencing: Any | None
    cha_list: Any | None
    comment_filter_status: int | None
    comment_setting: int | None
    commerce_user_level: int | None
    cover_url: list[HammerfestPonies] | None
    create_time: int | None
    download_prompt_ts: int | None
    download_setting: int | None
    duet_setting: int | None
    events: Any | None
    favoriting_count: int | None
    fb_expire_time: int | None
    follow_status: int | None
    follower_count: int | None
    follower_status: int | None
    followers_detail: Any | None
    following_count: int | None
    friends_status: int | None
    gender: int | None
    geofencing: list | None
    has_email: bool | None
    has_facebook_token: bool | None
    has_insights: bool | None
    has_orders: bool | None
    has_twitter_token: bool | None
    has_youtube_token: bool | None
    hide_search: bool | None
    homepage_bottom_toast: Any | None
    is_ad_fake: bool | None
    is_block: bool | None
    is_discipline_member: bool | None
    is_phone_binded: bool | None
    is_star: bool | None
    item_list: Any | None
    language: str | None
    live_agreement: int | None
    live_agreement_time: int | None
    live_commerce: bool | None
    live_verify: int | None
    matched_friend: MatchedFriend | None
    mutual_relation_avatars: Any | None
    need_points: Any | None
    need_recommend: int | None
    nickname: str | None
    platform_sync_info: Any | None
    prevent_download: bool | None
    react_setting: int | None
    reflow_page_gid: int | None
    reflow_page_uid: int | None
    region: str | None
    relative_users: Any | None
    room_id: int | None
    search_highlight: Any | None
    secret: int | None
    share_info: AuthorShareInfo | None
    shield_comment_notice: int | None
    shield_digg_notice: int | None
    shield_edit_field_info: Any | None
    shield_follow_notice: int | None
    short_id: int | None
    show_image_bubble: bool | None
    signature: str | None
    special_lock: int | None
    status: int | None
    stitch_setting: int | None
    total_favorited: int | None
    tw_expire_time: int | None
    type_label: list | None
    uid: str | None
    unique_id: str | None
    unique_id_modify_time: int | None
    user_canceled: bool | None
    user_mode: int | None
    user_period: int | None
    user_profile_guide: Any | None
    user_rate: int | None
    user_tags: Any | None
    verification_type: int | None
    video_icon: HammerfestPonies | None
    white_cover_url: Any | None
    with_commerce_entry: bool | None
    with_fusion_shop_entry: bool | None
    with_shop_entry: bool | None
    youtube_expire_time: int | None


class ChaList(BaseModel):
    author: dict[str, Any] | None
    banner_list: Any | None
    cha_attrs: Any | None
    cha_name: str | None
    cid: int | None
    collect_stat: int | None
    connect_music: list | None
    is_challenge: int | None
    is_commerce: bool | None
    is_pgcshow: bool | None
    schema_: str | None = Field(None, alias="schema")
    search_highlight: Any | None
    share_info: ChaListShareInfo | None
    show_items: Any | None
    sub_type: int | None
    type: int | None
    user_count: int | None
    view_count: int | None


class ImagePostInfo(BaseModel):
    image_post_cover: Image | None
    images: list[Image] | None


class YtInfo(BaseModel):
    album: Any | None
    artist: str | None
    availability: Any | None
    comment_count: int | None
    creator: str | None
    description: str | None
    duration: int | None
    extractor: str | None
    extractor_key: str | None
    formats: list[Format] | None
    id: str | None
    like_count: int | None
    repost_count: int | None
    subtitles: Subtitles | None
    thumbnails: list[Thumbnail] | None
    timestamp: int | None
    title: str | None
    track: str | None
    uploader: str | None
    uploader_id: str | None
    uploader_url: str | None
    view_count: int | None
    webpage_url: str | None


class TikTokAwmeRaw(BaseModel):
    anchors: Any | None
    author: Author | None
    author_user_id: int | None
    aweme_id: str | None
    aweme_type: int | None
    bodydance_score: int | None
    branded_content_accounts: Any | None
    cha_list: list[ChaList] | None
    challenge_position: Any | None
    cmt_swt: bool | None
    collect_stat: int | None
    commerce_config_data: Any | None
    content_desc_extra: list | None
    cover_labels: Any | None
    create_time: int | None
    desc: str | None
    desc_language: str | None
    disable_search_trending_bar: bool | None
    distribute_type: int | None
    duration: int | None
    follow_up_publish_from_id: int | None
    geofencing: list | None
    geofencing_regions: Any | None
    green_screen_materials: Any | None
    group_id: str | None
    hybrid_label: Any | None
    image_infos: Any | None
    image_post_info: ImagePostInfo | None
    interaction_stickers: Any | None
    is_ads: bool | None
    is_description_translatable: bool | None
    is_hash_tag: int | None
    is_pgcshow: bool | None
    is_relieve: bool | None
    is_text_sticker_translatable: bool | None
    is_top: int | None
    is_vr: bool | None
    item_comment_settings: int | None
    item_distribute_source: str | None
    item_duet: int | None
    item_react: int | None
    item_source_category: int | None
    label_top: HammerfestPonies | None
    label_top_text: Any | None
    long_video: Any | None
    mask_infos: list | None
    misc_info: str | None
    music: Music | None
    music_begin_time_in_ms: int | None
    nickname_position: Any | None
    origin_comment_ids: Any | None
    playlist_blocked: bool | None
    position: Any | None
    prevent_download: bool | None
    products_info: Any | None
    question_list: Any | None
    rate: int | None
    region: str | None
    risk_infos: RiskInfos | None
    search_highlight: Any | None
    share_info: ChaListShareInfo | None
    share_url: str | None
    statistics: Statistics | None
    status: Status | None
    text_extra: list[TextExtra] | None
    text_sticker_major_lang: str | None
    uniqid_position: Any | None
    user_digged: int | None
    video: Video | None
    video_control: VideoControl | None
    video_labels: list | None
    video_text: list | None
    with_promotional_music: bool | None
    with_survey: bool | None
    yt_info: YtInfo | None