


from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Invoice as InvoiceModel, Customer as CustomerModel, InvoiceLine as InvoiceLineModel
from app.schemas.schemas import Invoice, InvoiceCreate, InvoiceWithLines, InvoiceLine, InvoiceLineCreate

router = APIRouter(
    prefix="/invoices",
    tags=["invoices"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Invoice])
def read_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    invoices = db.query(InvoiceModel).offset(skip).limit(limit).all()
    return invoices

@router.get("/{invoice_id}", response_model=InvoiceWithLines)
def read_invoice(invoice_id: int, db: Session = Depends(get_db)):
    db_invoice = db.query(InvoiceModel).filter(InvoiceModel.InvoiceId == invoice_id).first()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoice

@router.post("/", response_model=Invoice)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    # Validate customer
    customer = db.query(CustomerModel).filter(CustomerModel.CustomerId == invoice.CustomerId).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_invoice = InvoiceModel(**invoice.model_dump())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.put("/{invoice_id}", response_model=Invoice)
def update_invoice(invoice_id: int, invoice: InvoiceCreate, db: Session = Depends(get_db)):
    db_invoice = db.query(InvoiceModel).filter(InvoiceModel.InvoiceId == invoice_id).first()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Validate customer
    customer = db.query(CustomerModel).filter(CustomerModel.CustomerId == invoice.CustomerId).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Update invoice attributes
    for key, value in invoice.model_dump().items():
        setattr(db_invoice, key, value)
    
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.delete("/{invoice_id}", response_model=Invoice)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    db_invoice = db.query(InvoiceModel).filter(InvoiceModel.InvoiceId == invoice_id).first()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    db.delete(db_invoice)
    db.commit()
    return db_invoice

# Invoice Lines endpoints
@router.get("/{invoice_id}/lines", response_model=List[InvoiceLine])
def read_invoice_lines(invoice_id: int, db: Session = Depends(get_db)):
    # Check if invoice exists
    invoice = db.query(InvoiceModel).filter(InvoiceModel.InvoiceId == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    lines = db.query(InvoiceLineModel).filter(InvoiceLineModel.InvoiceId == invoice_id).all()
    return lines

@router.post("/{invoice_id}/lines", response_model=InvoiceLine)
def create_invoice_line(invoice_id: int, line: InvoiceLineCreate, db: Session = Depends(get_db)):
    # Check if invoice exists
    invoice = db.query(InvoiceModel).filter(InvoiceModel.InvoiceId == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Ensure the invoice ID in the path matches the one in the request body
    if line.InvoiceId != invoice_id:
        raise HTTPException(status_code=400, detail="Invoice ID in path does not match Invoice ID in request body")
    
    db_line = InvoiceLineModel(**line.model_dump())
    db.add(db_line)
    db.commit()
    db.refresh(db_line)
    
    # Update invoice total
    invoice_lines = db.query(InvoiceLineModel).filter(InvoiceLineModel.InvoiceId == invoice_id).all()
    total = sum(line.UnitPrice * line.Quantity for line in invoice_lines)
    invoice.Total = total
    db.commit()
    
    return db_line

@router.get("/customer/{customer_id}", response_model=List[Invoice])
def read_customer_invoices(customer_id: int, db: Session = Depends(get_db)):
    # Check if customer exists
    customer = db.query(CustomerModel).filter(CustomerModel.CustomerId == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    invoices = db.query(InvoiceModel).filter(InvoiceModel.CustomerId == customer_id).all()
    return invoices


