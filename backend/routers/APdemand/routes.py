from fastapi import APIRouter, HTTPException, Depends
from data.models.provisioning import AP_Demand, Demand_Details

from backend.services import ledger as crud
from backend.core.middleware import get_current_user, get_admin_user

router = APIRouter()


# Create a new demand doc
@router.post("/")
async def create_demand_doc(demand: AP_Demand, user=Depends(get_current_user)):
    return await crud.create_demand(demand)


# Get all demand docs
@router.get("/")
async def get_all_demand_docs(user=Depends(get_current_user)):
    return await crud.get_all_demands()


# Get one demand doc by its code
@router.get("/{equipment_code}")
async def get_demand_doc(equipment_code: str, user=Depends(get_current_user)):
    doc = await crud.get_demand_by_code(equipment_code)
    if not doc:
        raise HTTPException(status_code=404, detail="Demand not found")
    return doc


# Add a detail line to a demand doc
@router.post("/{equipment_code}/add-detail")
async def add_detail_entry(
    equipment_code: str, detail: Demand_Details, admin=Depends(get_admin_user)
):
    success = await crud.add_demand_detail(equipment_code, detail)
    if not success:
        raise HTTPException(
            status_code=404, detail="Equipment code not found or add failed"
        )
    return {"status": "detail added"}


# Update a specific detail line
@router.put("/update-detail/{sub_dem_no}")
async def update_detail_entry(
    sub_dem_no: int, data: dict, admin=Depends(get_admin_user)
):
    success = await crud.update_demand_detail(sub_dem_no, data)
    if not success:
        raise HTTPException(404, "Detail not found or update failed")
    return {"status": "updated"}


# Search all demands
@router.get("/search/")
async def search_all_demands(query: str, user=Depends(get_current_user)):
    return await crud.search_demands(query)


# Filter demands by a field
@router.get("/filter/")
async def filter_all_demands(field: str, value: str, user=Depends(get_current_user)):
    return await crud.filter_demands(field, value)


# Get analytics
@router.get("/analysis/summary")
async def get_demand_summary(admin=Depends(get_admin_user)):
    return await crud.get_demand_analysis()
