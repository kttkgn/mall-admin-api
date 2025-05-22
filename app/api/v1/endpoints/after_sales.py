from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.services import after_sale as after_sale_service

router = APIRouter()

@router.get("/", response_model=schemas.AfterSaleList)
def read_after_sales(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    order_id: int = None,
    status: str = None,
    type: str = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取售后申请列表
    """
    after_sales = after_sale_service.get_after_sales(
        db, skip=skip, limit=limit, user_id=user_id, order_id=order_id, status=status, type=type
    )
    total = db.query(models.AfterSale).count()
    return {"total": total, "items": after_sales}

@router.post("/", response_model=schemas.AfterSale)
def create_after_sale(
    *,
    db: Session = Depends(deps.get_db),
    after_sale_in: schemas.AfterSaleCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    创建售后申请
    """
    try:
        after_sale = after_sale_service.create_after_sale(db, after_sale_in, current_user.id)
        return after_sale
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{after_sale_id}", response_model=schemas.AfterSale)
def read_after_sale(
    *,
    db: Session = Depends(deps.get_db),
    after_sale_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取售后申请详情
    """
    after_sale = after_sale_service.get_after_sale(db, after_sale_id)
    if not after_sale:
        raise HTTPException(status_code=404, detail="售后申请不存在")
    return after_sale

@router.put("/{after_sale_id}", response_model=schemas.AfterSale)
def update_after_sale(
    *,
    db: Session = Depends(deps.get_db),
    after_sale_id: int,
    after_sale_in: schemas.AfterSaleUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    更新售后申请
    """
    after_sale = after_sale_service.update_after_sale(
        db, after_sale_id, after_sale_in, operator=f"admin_{current_user.id}"
    )
    if not after_sale:
        raise HTTPException(status_code=404, detail="售后申请不存在")
    return after_sale

@router.get("/{after_sale_id}/logs", response_model=schemas.AfterSaleLogList)
def read_after_sale_logs(
    *,
    db: Session = Depends(deps.get_db),
    after_sale_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取售后申请日志
    """
    logs = after_sale_service.get_after_sale_logs(db, after_sale_id, skip, limit)
    total = db.query(models.AfterSaleLog).filter(models.AfterSaleLog.after_sale_id == after_sale_id).count()
    return {"total": total, "items": logs}

@router.post("/{after_sale_id}/logs", response_model=schemas.AfterSaleLog)
def create_after_sale_log(
    *,
    db: Session = Depends(deps.get_db),
    after_sale_id: int,
    log_in: schemas.AfterSaleLogCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    创建售后申请日志
    """
    after_sale = after_sale_service.get_after_sale(db, after_sale_id)
    if not after_sale:
        raise HTTPException(status_code=404, detail="售后申请不存在")
    log = after_sale_service.create_after_sale_log(db, after_sale_id, log_in)
    return log 