




from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Employee as EmployeeModel
from app.schemas.schemas import Employee, EmployeeCreate

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = db.query(EmployeeModel).offset(skip).limit(limit).all()
    return employees

@router.get("/{employee_id}", response_model=Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.EmployeeId == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.post("/", response_model=Employee)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # Validate reports_to if provided
    if employee.ReportsTo:
        reports_to = db.query(EmployeeModel).filter(EmployeeModel.EmployeeId == employee.ReportsTo).first()
        if not reports_to:
            raise HTTPException(status_code=404, detail="Manager not found")
    
    db_employee = EmployeeModel(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.put("/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.EmployeeId == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Validate reports_to if provided
    if employee.ReportsTo:
        # Ensure employee is not reporting to themselves
        if employee.ReportsTo == employee_id:
            raise HTTPException(status_code=400, detail="Employee cannot report to themselves")
        
        reports_to = db.query(EmployeeModel).filter(EmployeeModel.EmployeeId == employee.ReportsTo).first()
        if not reports_to:
            raise HTTPException(status_code=404, detail="Manager not found")
    
    # Update employee attributes
    for key, value in employee.model_dump().items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/{employee_id}", response_model=Employee)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.EmployeeId == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check if employee has subordinates
    subordinates = db.query(EmployeeModel).filter(EmployeeModel.ReportsTo == employee_id).all()
    if subordinates:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete employee with subordinates. Reassign subordinates first."
        )
    
    db.delete(db_employee)
    db.commit()
    return db_employee

@router.get("/{employee_id}/subordinates", response_model=List[Employee])
def read_employee_subordinates(employee_id: int, db: Session = Depends(get_db)):
    # Check if employee exists
    employee = db.query(EmployeeModel).filter(EmployeeModel.EmployeeId == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    subordinates = db.query(EmployeeModel).filter(EmployeeModel.ReportsTo == employee_id).all()
    return subordinates




