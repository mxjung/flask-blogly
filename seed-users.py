"""Seed file to make sample data for pets db."""
from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add Users
max = User(first_name='Max', last_name='Jung', image_url="https://4.bp.blogspot.com/-Nxb3PYLE0o4/UqnX12lzS9I/AAAAAAAAKqc/dHIj8ArQqZ4/s1600/00-Front-Image-Morgan-Freeman-Visual-Artist-Kyle-Lambert-iPad-Hyper-realistic-Portraits-www-designstack-co.jpg")
megan = User(first_name='Megan', last_name='Stormborn', image_url="https://kottke.org/plus/misc/images/ai-faces-01.jpg")
spike = User(first_name='Spike', last_name='From Buffy', image_url="https://i.pinimg.com/originals/be/89/d0/be89d00331f2f22f86488a5d12fe518b.jpg")

# Add new users to session, so they'll persist
db.session.add(max)
db.session.add(megan)
db.session.add(spike)

# Commit users --otherwise, this never gets saved!
db.session.commit()

# Add posts
max_post = Post(title='hello world', content='its me', user_id=1)
blob = Post(title='WTF', content='i hate databases', user_id=2)
whatever = Post(title='lorum ipsum', content='solor dit', user_id=1)
hello = Post(title='goodbye everyone', content='im fine just leaving', user_id=3)

# Now add new posts to session
db.session.add(max_post)
db.session.add(blob)
db.session.add(whatever)
db.session.add(hello)
db.session.commit()
