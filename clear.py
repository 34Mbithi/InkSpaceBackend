from server import create_app, db
from server.models import User, BlogPost, Category, Comment
from seed import seed_data 

def clear_data():
    # Clear all data in tables
    db.session.query(User).delete()
    db.session.query(BlogPost).delete()
    db.session.query(Category).delete()
    db.session.query(Comment).delete()
    db.session.commit()
    print("All data cleared.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        clear_data()
        seed_data()
        print("Database re-seeded successfully!")
