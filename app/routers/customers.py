


from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Customer as CustomerModel, Employee as EmployeeModel
from app.schemas.schemas import Customer, CustomerCreate, CustomerWithInvoices

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(CustomerModel).offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(CustomerModel).filter(CustomerModel.CustomerId == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.get("/{customer_id}/with-invoices", response_model=CustomerWithInvoices)
def read_customer_with_invoices(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(CustomerModel).filter(CustomerModel.CustomerId == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.post("/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    # Validate support rep if provided
    if customer.SupportRepId:
        support_rep = db.query(EmployeeModel).filter(EmployeeModel.EmployeeId == customer.SupportRepId).first()
        if not support_rep:
            raise HTTPException(status_code=404, detail="Support representative not found")
    
    db_customer = CustomerModel(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(CustomerModel).filter(CustomerModel.CustomerId == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Validate support rep if provided
    if customer.SupportRepId:
        support_rep = db.query(EmployeeModel).filter(EmployeeModel.EmployeeId == customer.SupportRepId).first()
        if not support_rep:
            raise HTTPException(status_code=404, detail="Support representative not found")
    
    # Update customer attributes
    for key, value in customer.model_dump().items():
        setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}", response_model=Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(CustomerModel).filter(CustomerModel.CustomerId == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    return db_customer

@router.get("/search/{query}", response_model=List[Customer])
def search_customers(query: str, db: Session = Depends(get_db)):
    customers = db.query(CustomerModel).filter(
        (CustomerModel.FirstName.like(f"%{query}%")) | 
        (CustomerModel.LastName.like(f"%{query}%")) |
        (CustomerModel.Email.like(f"%{query}%")) |
        (CustomerModel.Company.like(f"%{query}%"))
    ).all()
    return customers


