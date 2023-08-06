# -*- coding: utf-8 -*-
import datetime
from typing import Optional, List, Any

from requests_toolbelt.utils import deprecated
from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList, TDict
from owlmixin.owlenum import OwlEnum
from requests.structures import CaseInsensitiveDict as RequestsCaseInsensitiveDict

DictOrList = any

def to_json(value: DictOrList) -> str: 
    if isinstance(value, dict):
        return TDict(value).to_json()
    if isinstance(value, list):
        return TList(value).to_json()
    return None


class CaseInsensitiveDict(RequestsCaseInsensitiveDict):
    pass


class NotifierType(OwlEnum):
    SLACK = "slack"


class Status(OwlEnum):
    SAME = "same"
    DIFFERENT = "different"
    FAILURE = "failure"


class HttpMethod(OwlEnum):
    GET = "GET"
    POST = "POST"


class QueryCustomization(OwlMixin):
    overwrite: TOption[TDict[TList[str]]]
    remove: TOption[TList[str]]


class PathReplace(OwlMixin):
    before: str
    after: str


class AccessPoint(OwlMixin):
    name: str
    host: str
    path: TOption[PathReplace]
    query: TOption[QueryCustomization]
    proxy: TOption[str]
    default_response_encoding: TOption[str]
    headers: TDict[str] = {}


class OutputSummary(OwlMixin):
    response_dir: str
    encoding: str = "utf8"
    logger: TOption[any]


class Concurrency(OwlMixin):
    threads: int
    processes: int


class Addon(OwlMixin):
    name: str
    cls_name: str = "Executor"
    config: TOption[dict]
    include: TOption[str]
    tags: TOption[TList[str]]


# List is None...
class Addons(OwlMixin):
    log2reqs: Addon
    reqs2reqs: TList[Addon] = []
    res2res: TList[Addon] = []
    res2dict: TList[Addon] = []
    judgement: TList[Addon] = []
    store_criterion: TList[Addon] = []
    dump: TList[Addon] = []
    did_challenge: TList[Addon] = []
    final: TList[Addon] = []


class Notifier(OwlMixin):
    type: NotifierType
    channel: str
    username: str = "jumeaux"
    icon_emoji: TOption[str]
    icon_url: TOption[str]

    @property
    def logging_message(self) -> str:
        return f"Send to {self.channel} by slack"


class Config(OwlMixin):
    one: AccessPoint
    other: AccessPoint
    output: OutputSummary
    threads: int = 1
    processes: TOption[int]
    max_retries: int = 3
    title: TOption[str]
    description: TOption[str]
    tags: TOption[TList[str]]
    # TODO: remove
    input_files: TOption[TList[str]]
    notifiers: TOption[TDict[Notifier]]
    addons: Addons


# --------


class Args(OwlMixin):
    run: bool
    files: TOption[TList[str]]
    title: TOption[str]
    description: TOption[str]
    config: TOption[TList[str]]
    tag: TOption[TList[str]]
    skip_addon_tag: TOption[TList[str]]
    threads: TOption[int]
    processes: TOption[int]
    max_retries: TOption[int]
    v: int
    retry: bool
    report: TOption[str]  # Only case in which retry is True

    init: bool
    name: TOption[str]  # Only case in which init is True
    server: bool
    port: int
    viewer: bool
    responses_dir: str

    @classmethod
    def ___threads(cls, v: Optional[str]) -> Optional[int]:
        return int(v) if v else None

    @classmethod
    def ___processes(cls, v: Optional[str]) -> Optional[int]:
        return int(v) if v else None

    @classmethod
    def ___max_retries(cls, v: Optional[str]) -> Optional[int]:
        return int(v) if v else None

    @classmethod
    def ___port(cls, v: str) -> int:
        return int(v)


# or {}
class Request(OwlMixin):
    name: TOption[str]
    method: HttpMethod = HttpMethod.GET
    path: str
    qs: TDict[TList[str]] = {}
    form: TOption[dict]
    json: TOption[dict]
    headers: TDict[str] = {}
    url_encoding: str = "utf-8"


class Proxy(OwlMixin):
    http: str
    https: str

    @classmethod
    def from_host(cls, host: TOption[str]) -> "Proxy":
        return (
            Proxy.from_dict({"http": f"http://{host.get()}", "https": f"https://{host.get()}"})
            if not host.is_none()
            else None
        )


class Response(OwlMixin):
    body: bytes
    encoding: TOption[str]
    headers: CaseInsensitiveDict
    url: str
    status_code: int
    elapsed: datetime.timedelta
    elapsed_sec: float
    type: str

    @property
    def text(self) -> str:
        # Refer https://github.com/requests/requests/blob/e4fc3539b43416f9e9ba6837d73b1b7392d4b242/requests/models.py#L831
        return self.body.decode(self.encoding.get_or("utf8"), errors="replace")

    @property
    def byte(self) -> int:
        return len(self.body)

    @property
    def content_type(self) -> TOption[str]:
        return TOption(self.headers.get("content-type"))

    @property
    def mime_type(self) -> TOption[str]:
        return self.content_type.map(lambda x: x.split(";")[0])

    @property
    def charset(self) -> TOption[str]:
        return self.content_type.map(lambda x: x.split(";")[1] if x.split(";") > 1 else None)

    @property
    def ok(self) -> bool:
        return self.status_code == 200

    @classmethod
    def ___headers(cls, v):
        return CaseInsensitiveDict(v)

    @classmethod
    def _decide_encoding(
        cls, res: Any, default_encoding: TOption[str] = TOption(None)
    ) -> Optional[str]:
        content_type = res.headers.get("content-type")

        if content_type and "octet-stream" in content_type:
            return None
        # XXX: See 2.2 in https://tools.ietf.org/html/rfc2616#section-2.2
        if res.encoding and not ("text" in content_type and res.encoding == "ISO-8859-1"):
            return res.encoding

        meta_encodings: List[str] = deprecated.get_encodings_from_content(res.content)
        return (
            meta_encodings[0] if meta_encodings else default_encoding.get() or res.apparent_encoding
        )

    @classmethod
    def _to_type(cls, res: Any) -> str:
        content_type = res.headers.get("content-type")
        if not content_type:
            return "unknown"
        return content_type.split(";")[0].split("/")[1]

    @classmethod
    def from_requests(cls, res: Any, default_encoding: TOption[str] = TOption(None)) -> "Response":
        encoding: Optional[str] = cls._decide_encoding(res, default_encoding)
        type: str = cls._to_type(res)
        return Response.from_dict(
            {
                "body": res.content,
                "encoding": encoding,
                "headers": res.headers,
                "url": res.url,
                "status_code": res.status_code,
                "elapsed": res.elapsed,
                "elapsed_sec": round(res.elapsed.seconds + res.elapsed.microseconds / 1000000, 2),
                "type": type,
            }
        )


# --------


class ChallengeArg(OwlMixin):
    seq: int
    number_of_request: int
    key: str
    session: object
    req: Request
    host_one: str
    host_other: str
    path_one: TOption[PathReplace]
    path_other: TOption[PathReplace]
    query_one: TOption[QueryCustomization]
    query_other: TOption[QueryCustomization]
    proxy_one: TOption[Proxy]
    proxy_other: TOption[Proxy]
    headers_one: TDict[str]
    headers_other: TDict[str]
    default_response_encoding_one: TOption[str]
    default_response_encoding_other: TOption[str]
    res_dir: str


# --------


class StatusCounts(OwlMixin):
    same: int = 0
    different: int = 0
    failure: int = 0


class Time(OwlMixin):
    start: str  # yyyy/MM/dd hh:mm:ss
    end: str  # yyyy/MM/dd hh:mm:ss
    elapsed_sec: int


class Summary(OwlMixin):
    one: AccessPoint
    other: AccessPoint
    status: StatusCounts
    tags: TList[str]
    time: Time
    concurrency: Concurrency
    output: OutputSummary
    default_encoding: TOption[str]


class DiffKeys(OwlMixin):
    added: TList[str]
    changed: TList[str]
    removed: TList[str]

    def is_empty(self) -> bool:
        return len(self.added) == len(self.changed) == len(self.removed) == 0

    @classmethod
    def empty(cls) -> "DiffKeys":
        return DiffKeys.from_dict({"added": [], "changed": [], "removed": []})


class ResponseSummary(OwlMixin):
    url: str
    type: str
    status_code: TOption[int]
    byte: TOption[int]
    response_sec: TOption[float]
    content_type: TOption[str]
    mime_type: TOption[str]
    encoding: TOption[str]
    file: TOption[str]
    prop_file: TOption[str]


class Trial(OwlMixin):
    """ Affect `final/csv` config specifications,
    """

    seq: int
    name: str
    tags: TList[str]
    headers: TDict[str]
    queries: TDict[TList[str]]
    form: TOption[dict]
    json: TOption[dict]
    one: ResponseSummary
    other: ResponseSummary
    method: HttpMethod
    path: str
    request_time: str
    status: Status
    # `None` is not same as `{}`. `{}` means no diffs, None means unknown
    diffs_by_cognition: TOption[TDict[DiffKeys]]


class Report(OwlMixin):
    """ Affect `final/slack` config specifications,
    """

    version: str
    key: str
    title: str
    description: TOption[str]
    summary: Summary
    trials: TList[Trial]
    addons: TOption[Addons]
    retry_hash: TOption[str]


# ---


class Log2ReqsAddOnPayload(OwlMixin):
    file: str


class Reqs2ReqsAddOnPayload(OwlMixin):
    requests: TList[Request]


class DumpAddOnPayload(OwlMixin):
    response: Response
    body: bytes
    encoding: TOption[str]


class Res2ResAddOnPayload(OwlMixin):
    response: Response
    req: Request
    tags: TList[str]


class Res2DictAddOnPayload(OwlMixin):
    response: Response
    result: TOption[DictOrList]


class DidChallengeAddOnPayload(OwlMixin):
    trial: Trial


class DidChallengeAddOnReference(OwlMixin):
    res_one: Response
    res_other: Response
    res_one_props: TOption[DictOrList]
    res_other_props: TOption[DictOrList]


class JudgementAddOnPayload(OwlMixin):
    # By ignores title in config.yml
    # `unknown` is diffs which didn't match any configurations
    diffs_by_cognition: TOption[TDict[DiffKeys]]
    regard_as_same: bool


class JudgementAddOnReference(OwlMixin):
    name: str
    path: str
    qs: TDict[TList[str]]
    headers: TDict[str]
    res_one: Response
    res_other: Response
    dict_one: TOption[DictOrList]
    dict_other: TOption[DictOrList]


class StoreCriterionAddOnPayload(OwlMixin):
    stored: bool


class StoreCriterionAddOnReference(OwlMixin):
    status: Status
    req: Request
    res_one: Response
    res_other: Response


class FinalAddOnPayload(OwlMixin):
    report: Report
    output_summary: OutputSummary

    @property
    def result_path(self) -> str:
        return f"{self.output_summary.response_dir}/{self.report.key}"


class FinalAddOnReference(OwlMixin):
    notifiers: TOption[TDict[Notifier]]
