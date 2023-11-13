# generated by datamodel-codegen:
#   timestamp: 2022-12-14T07:40:59+00:00


from __future__ import annotations

from melanie import BaseModel, Field


class Metrics(BaseModel):
    pass


class TopDoc(BaseModel):
    id: str | None
    text: str | None
    title: str | None


class BeamText(BaseModel):
    __root__: float | str | None = Field(None, title="BeamText")


class ChatAct(BaseModel):
    beam_texts: list[list[BeamText]] | None
    clen: int | None
    ctrunc: int | None
    ctrunclen: int | None
    doc_content: list[str] | None
    doc_titles: list[str] | None
    doc_urls: list[str] | None
    episode_done: bool | None
    gen_n_toks: int | None
    id: str | None
    knowledge_response: str | None
    metrics: Metrics | None
    search_decision: str | None
    search_query: str | None
    text: str | None
    top_docs: list[TopDoc] | None

    @classmethod
    def from_act(cls, res) -> ChatAct:
        data = {**res, "top_docs": [TopDoc(title=i.get_title(), text=i.get_passage_str(), id=i.get_id()) for i in res["top_docs"]], "metrics": {}}
        for k, v in res["metrics"].items():
            try:
                data[k] = v.value()
            except AttributeError:
                data[k] = v

        return cls(**data)