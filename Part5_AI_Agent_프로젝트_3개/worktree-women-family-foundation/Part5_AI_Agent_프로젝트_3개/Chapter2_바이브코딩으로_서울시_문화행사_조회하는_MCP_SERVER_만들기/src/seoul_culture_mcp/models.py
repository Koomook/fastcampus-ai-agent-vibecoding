from pydantic import BaseModel, Field
from typing import Optional, List


class CulturalEvent(BaseModel):
    """문화행사 데이터 모델"""
    codename: str = Field(description="행사 분류")
    title: str = Field(description="공연/행사명")
    date: str = Field(description="행사 기간")
    place: str = Field(description="장소")
    org_name: str = Field(description="주최 기관")
    use_trgt: Optional[str] = Field(description="이용대상")
    use_fee: Optional[str] = Field(description="이용요금")
    is_free: str = Field(description="유무료 구분")
    guname: str = Field(description="자치구")
    lat: Optional[str] = Field(description="위도")
    lot: Optional[str] = Field(description="경도")
    main_img: Optional[str] = Field(description="대표 이미지 URL")
    hmpg_addr: Optional[str] = Field(description="문화포털 상세 URL")
    org_link: Optional[str] = Field(description="주최 기관 링크")


class APIResponse(BaseModel):
    """API 응답 모델"""
    list_total_count: int
    result_code: str
    result_message: str
    events: List[CulturalEvent]
