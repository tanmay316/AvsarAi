from api import app, db

with app.app_context():
    db.drop_all()  # Drop existing tables
    db.create_all()  # Create new tables with updated schema
    print("Database tables created successfully!") 