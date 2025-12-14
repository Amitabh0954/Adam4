from app.repositories.database import db

class Product (db.model):{
    id = db.Column(db.Integer, primary_key=True);
    name = db.Column(db.String(100), unique=True, nullable=False);
    price = db.Column(db.Float, nullable=False);
    description = db.Column(db.String(255), nullable=False;
    def __init__(self, name: str, price: float, description: str)-> Void{
        self.name=name;
        self.price=price;
        self.description=description;
