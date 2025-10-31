from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
import re
from data.database import MongoManager
from data.models.apdemand import APDemandCreate, APDemandUpdate

mongo_manager = MongoManager()

def serialize_doc(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

#  Create a new Advance Provisioning or Supplementary Demand
async def create_ap_demand(ap_data: APDemandCreate):
    collection = mongo_manager.ap_demand

    ap_data_dict = ap_data.dict()
    ap_data_dict["created_at"] = datetime.utcnow()

    result = await collection.insert_one(ap_data_dict)
    return {"_id": str(result.inserted_id), "message": "AP Demand created successfully"}

#  Get all demands (both AP and Supplementary)
async def get_all_demands():
    collection = mongo_manager.ap_demand
    demands = await collection.find({}).to_list(None)
    return [serialize_doc(d) for d in demands]

#  Get demands by equipment code
async def get_demands_by_equipment(equipment_code: str):
    collection = mongo_manager.ap_demand
    pattern = f"^{re.escape(equipment_code)}$"
    docs = await collection.find({"equipment_code": {"$regex": pattern, "$options": "i"}}).to_list(None)
    return [serialize_doc(d) for d in docs]

#  Update an existing demand
async def update_ap_demand(demand_id: str, update_data: APDemandUpdate):
    collection = mongo_manager.ap_demand
    filtered_data = {k: v for k, v in update_data.dict().items() if v not in (None, "", [], {})}
    
    result = await collection.update_one({"_id": ObjectId(demand_id)}, {"$set": filtered_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Demand not found or no changes applied.")
    return {"status": "updated successfully"}

#  Delete a demand
async def delete_ap_demand(demand_id: str):
    collection = mongo_manager.ap_demand
    result = await collection.delete_one({"_id": ObjectId(demand_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Demand not found.")
    return {"status": "deleted successfully"}
