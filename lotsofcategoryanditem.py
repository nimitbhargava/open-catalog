# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Item, User, Base

engine = create_engine('sqlite:///opencatalog.db')

# Clear database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create a user
nimit = User(name="Nimit Bhargava", email="nimitbhargava@gmail.com")
session.add(nimit)
session.commit()

rajasthan = Category(name="Rajasthan", owner_id=1)
session.add(rajasthan)
session.commit()

# Items for Rajasthan
ajmer = Item(title="Ajmer", owner_id=1,
             description="Ajmer is a city in the northern Indian state of Rajasthan. South of the city's artificial Ana Sagar Lake is Ajmer Sharif Dargah, the domed shrine of the Muslim Sufi saint Garib Nawaz.",
             category=rajasthan)
session.add(ajmer)
session.commit()

jaipur = Item(title="Jaipur", owner_id=1,
              description="Jaipur is the capital of IndiaRajasthan state. It evokes the royal family that once ruled the region and that, in 1727.",
              category=rajasthan)
session.add(jaipur)
session.commit()

maharashtra = Category(name="Maharashtra", owner_id=1)
session.add(maharashtra)
session.commit()

# Items for Maharashtra
mumbai = Item(title="Mumbai", owner_id=1,
              description="Mumbai (formerly called Bombay) is a densely populated city on Indiawest coast. A financial center, it's India's largest city. On the Mumbai Harbour waterfront stands the iconic Gateway of India stone arch.",
              category=maharashtra)
session.add(mumbai)
session.commit()

pune = Item(title="Pune", owner_id=1,
            description="Pune is a sprawling city in the western Indian state of Maharashtra. It was once the base of the Peshwas (prime ministers) of the Maratha Empire, which lasted from 1674 to 1818.",
            category=maharashtra)
session.add(pune)
session.commit()

karnataka = Category(name="Karnataka", owner_id=1)
session.add(karnataka)
session.commit()

# Items for Karnataka
bangalore = Item(title="Bangalore", owner_id=1,
                 description="Bengaluru (also called Bangalore) is the capital of India's southern Karnataka state. The center of India's high-tech industry, the city is also known for its parks and nightlife.",
                 category=karnataka)
session.add(bangalore)
session.commit()

mangalore = Item(title="Mangalore", owner_id=1,
                 description="Mangalore (or Mangaluru) is an Arabian Sea port and a major commercial center in the Indian state of Karnataka. It's home to the Kadri Manjunath Temple, known for its bronze statues, and the 9th-century Mangaladevi Temple.",
                 category=karnataka)
session.add(mangalore)
session.commit()

print
"Seeded database with categories and their items!"
