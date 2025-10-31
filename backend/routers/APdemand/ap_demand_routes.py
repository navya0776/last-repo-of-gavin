from fastapi import APIRouter, Depends, HTTPException
from backend.services import ap_demand_crud
from backend.core.middleware import get_current_user, get_admin_user
from data.models.apdemand import APDemandCreate, APDemandUpdate

router = APIRouter(prefix="/ap-demand", tags=["Advance Provisioning Demand"])

#  Create new AP/ Supplementary Demand
@router.post("/")
async def create_ap_demand(ap_data: APDemandCreate, user=Depends(get_current_user)):
    return await ap_demand_crud.create_ap_demand(ap_data)

#  Get all demands
@router.get("/")
async def get_all_demands(user=Depends(get_current_user)):
    return await ap_demand_crud.get_all_demands()

#  Get all demands by equipment
@router.get("/equipment/{equipment_code}")
async def get_demands_by_equipment(equipment_code: str, user=Depends(get_current_user)):
    demands = await ap_demand_crud.get_demands_by_equipment(equipment_code)
    if not demands:
        raise HTTPException(status_code=404, detail="No demands found for this equipment.")
    return demands

#  Update a demand
@router.put("/{demand_id}")
async def update_ap_demand(demand_id: str, update_data: APDemandUpdate, user=Depends(get_current_user)):
    return await ap_demand_crud.update_ap_demand(demand_id, update_data)

#  Delete a demand
@router.delete("/{demand_id}")
async def delete_ap_demand(demand_id: str, admin=Depends(get_admin_user)):
    return await ap_demand_crud.delete_ap_demand(demand_id)
