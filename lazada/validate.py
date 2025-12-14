from pydantic import BaseModel, Field
from typing import Optional, Literal

class LazadaCommonParams(BaseModel):
    app_key: str = Field(...,description="Unique app ID issued by Lazada Open Platform console")
    timestamp: str = Field(...,description="Request timestamp in milliseconds, must be within 7200s of UTC")
    access_token: str = Field(...,description="API interface call credentials")
    sign_method: str = "sha256"

class DiscoveryReportParams(LazadaCommonParams):
    # Required
    startDate: str = Field(...,description="Start date, format yyyy-MM-dd")
    endDate: str = Field(...,description="End date, format yyyy-MM-dd")
    pageNo: str = Field("1",description="Page number, default 1, max 100")
    pageSize: str = Field("100",description="Page size, default 10, max 100")
    
    # Optional
    campaignId: Optional[int] = Field(None, description="Campaign Id")
    useRtTable: Optional[bool] = Field(None,description="Use realtime data when endDate is today")
    sort: Optional[str] = Field(None,description="Sort column")
    order: Optional[Literal["ASC", "DESC"]] = Field(None,description="Sort order")
    campaignType: Optional[int] = Field(None,description="Campaign type: 1 Manual, 2 Automated")
    productType: Optional[Literal["N", "J"]] = Field(None,description="Placement: N Sponsored Search, J Sponsored Product")
    campaignName: Optional[str] = Field(None,description="Campaign name (fuzzy search)")