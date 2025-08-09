
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from app.database import Base

class Artist(Base):
    __tablename__ = "Artist"

    ArtistId = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    
    albums = relationship("Album", back_populates="artist")

class Album(Base):
    __tablename__ = "Album"

    AlbumId = Column(Integer, primary_key=True, index=True)
    Title = Column(String)
    ArtistId = Column(Integer, ForeignKey("Artist.ArtistId"))
    
    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album")

class Genre(Base):
    __tablename__ = "Genre"

    GenreId = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    
    tracks = relationship("Track", back_populates="genre")

class MediaType(Base):
    __tablename__ = "MediaType"

    MediaTypeId = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    
    tracks = relationship("Track", back_populates="media_type")

class Track(Base):
    __tablename__ = "Track"

    TrackId = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    AlbumId = Column(Integer, ForeignKey("Album.AlbumId"))
    MediaTypeId = Column(Integer, ForeignKey("MediaType.MediaTypeId"))
    GenreId = Column(Integer, ForeignKey("Genre.GenreId"))
    Composer = Column(String)
    Milliseconds = Column(Integer)
    Bytes = Column(Integer)
    UnitPrice = Column(Float)
    
    album = relationship("Album", back_populates="tracks")
    genre = relationship("Genre", back_populates="tracks")
    media_type = relationship("MediaType", back_populates="tracks")
    playlist_tracks = relationship("PlaylistTrack", back_populates="track")
    invoice_lines = relationship("InvoiceLine", back_populates="track")

class Playlist(Base):
    __tablename__ = "Playlist"

    PlaylistId = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    
    playlist_tracks = relationship("PlaylistTrack", back_populates="playlist")

class PlaylistTrack(Base):
    __tablename__ = "PlaylistTrack"

    PlaylistId = Column(Integer, ForeignKey("Playlist.PlaylistId"), primary_key=True)
    TrackId = Column(Integer, ForeignKey("Track.TrackId"), primary_key=True)
    
    playlist = relationship("Playlist", back_populates="playlist_tracks")
    track = relationship("Track", back_populates="playlist_tracks")

class Customer(Base):
    __tablename__ = "Customer"

    CustomerId = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String)
    LastName = Column(String)
    Company = Column(String)
    Address = Column(String)
    City = Column(String)
    State = Column(String)
    Country = Column(String)
    PostalCode = Column(String)
    Phone = Column(String)
    Fax = Column(String)
    Email = Column(String)
    SupportRepId = Column(Integer, ForeignKey("Employee.EmployeeId"))
    
    support_rep = relationship("Employee", back_populates="customers")
    invoices = relationship("Invoice", back_populates="customer")

class Employee(Base):
    __tablename__ = "Employee"

    EmployeeId = Column(Integer, primary_key=True, index=True)
    LastName = Column(String)
    FirstName = Column(String)
    Title = Column(String)
    ReportsTo = Column(Integer, ForeignKey("Employee.EmployeeId"))
    BirthDate = Column(DateTime)
    HireDate = Column(DateTime)
    Address = Column(String)
    City = Column(String)
    State = Column(String)
    Country = Column(String)
    PostalCode = Column(String)
    Phone = Column(String)
    Fax = Column(String)
    Email = Column(String)
    
    reports_to = relationship("Employee", remote_side=[EmployeeId], backref="subordinates")
    customers = relationship("Customer", back_populates="support_rep")

class Invoice(Base):
    __tablename__ = "Invoice"

    InvoiceId = Column(Integer, primary_key=True, index=True)
    CustomerId = Column(Integer, ForeignKey("Customer.CustomerId"))
    InvoiceDate = Column(DateTime)
    BillingAddress = Column(String)
    BillingCity = Column(String)
    BillingState = Column(String)
    BillingCountry = Column(String)
    BillingPostalCode = Column(String)
    Total = Column(Float)
    
    customer = relationship("Customer", back_populates="invoices")
    invoice_lines = relationship("InvoiceLine", back_populates="invoice")

class InvoiceLine(Base):
    __tablename__ = "InvoiceLine"

    InvoiceLineId = Column(Integer, primary_key=True, index=True)
    InvoiceId = Column(Integer, ForeignKey("Invoice.InvoiceId"))
    TrackId = Column(Integer, ForeignKey("Track.TrackId"))
    UnitPrice = Column(Float)
    Quantity = Column(Integer)
    
    invoice = relationship("Invoice", back_populates="invoice_lines")
    track = relationship("Track", back_populates="invoice_lines")
