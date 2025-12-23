from ..extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List

class Customers(db.Model):
    __tablename__ = 'customers'
    CustomerId: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    Email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    DOB: Mapped[date] = mapped_column(db.Date)
    Password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    Address: Mapped[str] = mapped_column(db.String(255), nullable=False)
    PhoneNumber: Mapped[str] = mapped_column(db.String(20), nullable=False)
    ServiceTickets: Mapped[List["Service_Tickets"]] = relationship("Service_Tickets", back_populates="Customer")

class Service_Tickets(db.Model):
    __tablename__ = 'service_tickets'
    TicketId: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    CustomerId: Mapped[int] = mapped_column(db.ForeignKey('customers.CustomerId'), nullable=False)
    MechanicId: Mapped[int] = mapped_column(db.ForeignKey('mechanics.MechanicID'), nullable=True)
    Description: Mapped[str] = mapped_column(db.String(255), nullable=False)
    Status: Mapped[str] = mapped_column(db.String(50), nullable=False)
    CreatedAt: Mapped[date] = mapped_column(db.Date, nullable=False)
    Customer: Mapped["Customers"] = relationship("Customers", back_populates="ServiceTickets")
    Mechanic: Mapped["Mechanics"] = relationship("Mechanics", back_populates="ServiceTickets")

class Service_Tickets_Mechanics(db.Model):
    __tablename__ = "service_tickets_mechanics"
    Id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    TicketId: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.TicketId'), nullable=False)
    MechanicId: Mapped[int] = mapped_column(db.ForeignKey('mechanics.MechanicID'), nullable=False)
    Role: Mapped[str] = mapped_column(db.String(100), nullable=False)
    HoursWorked: Mapped[float] = mapped_column(db.Float, nullable=False)

class Mechanics(db.Model):
    __tablename__ = 'mechanics'
    MechanicID: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    Email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    Address: Mapped[str] = mapped_column(db.String(255), nullable=False)
    PhoneNumber: Mapped[str] = mapped_column(db.String(20), nullable=False)
    Salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    ServiceTickets: Mapped[List["Service_Tickets"]] = relationship("Service_Tickets", back_populates="Mechanic")
