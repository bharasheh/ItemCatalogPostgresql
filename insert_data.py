#!/usr/bin/env python2
#
# Insert testing data in Item Catalog database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem

engine = create_engine("postgresql://catalog:catalog@localhost:5432/catalog")
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


# Category for Soccer
category1 = Category(name="Soccer")
session.add(category1)
session.commit()

categoryItem11 = CategoryItem(title="Manchester United", description=""
                              + "Manchester United Football Club is an "
                              + "English Premier League football club that "
                              + "plays at Old Trafford in Greater Manchester "
                              + "and is one of the most successful clubs in "
                              + " Europe. The club was formed in 1878, as the "
                              + "team Newton Heath F.C. It joined the "
                              + "Football League in 1892, and have only been "
                              + "relegated once since 1938. The mean "
                              + "attendances of the games are higher than any "
                              + "English football league team for all but six "
                              + "seasons starting in 1964. The team won 38 "
                              + "trophies under Alex Ferguson.",
                              category=category1)
session.add(categoryItem11)
session.commit()

categoryItem12 = CategoryItem(title="Arsenal", description="Known by the "
                              + "nickname of The Gunners, Arsenal are old "
                              + "rivals of both, Manchester United and "
                              + "Chelsea. Arsenal are currently playing in "
                              + "the new Emirates Stadium.",
                              category=category1)
session.add(categoryItem12)
session.commit()

categoryItem13 = CategoryItem(title="Chelsea", description="Known by the "
                              + "nickname of The Blues, they play at Stamford"
                              + " Bridge and are currently managed by Antonio"
                              + " Conte. They are currently owned by Russian "
                              + "oil-baron Roman Abramovich.",
                              category=category1)
session.add(categoryItem13)
session.commit()

categoryItem14 = CategoryItem(title="Liverpool", description="Liverpool "
                              + "Football Club is a Premier League football "
                              + "club based in Liverpool. Liverpool F.C. is "
                              + "one of the most successful clubs in England "
                              + "and has won more European trophies than any "
                              + "other English team with five European Cups, "
                              + "three UEFA Cups, and three UEFA Super Cups. "
                              + "The club has also won eighteen League titles"
                              + ", seven FA Cups and a record eight League "
                              + "Cups. In spite of their successful history, "
                              + "Liverpool are yet to win a Premier League "
                              + "title since its inception in 1992.",
                              category=category1)
session.add(categoryItem14)
session.commit()


# Category for Basketball
category2 = Category(name="Basketball")
session.add(category2)
session.commit()

categoryItem21 = CategoryItem(title="Spain", description="Spain",
                              category=category2)
session.add(categoryItem21)
session.commit()

categoryItem22 = CategoryItem(title="Italy", description="Italy",
                              category=category2)
session.add(categoryItem22)
session.commit()

categoryItem23 = CategoryItem(title="Germany", description="Germany",
                              category=category2)
session.add(categoryItem23)
session.commit()


# Category for Baseball
category3 = Category(name="Baseball")
session.add(category3)
session.commit()

categoryItem31 = CategoryItem(title="Chicago White Sox", description="an "
                              + "American professional baseball team based in"
                              + " Chicago, Illinois. The White Sox compete in"
                              + " Major League Baseball (MLB) as a member "
                              + "club of the American League (AL) Central "
                              + "division.", category=category3)
session.add(categoryItem31)
session.commit()

categoryItem32 = CategoryItem(title="Cleveland Indians", description="an "
                              + "American professional baseball team based in"
                              + " Cleveland, Ohio. The Indians compete in "
                              + "Major League Baseball (MLB) as a member club"
                              + " of the American League (AL) Central "
                              + "division.", category=category3)
session.add(categoryItem32)
session.commit()

categoryItem33 = CategoryItem(title="Detroit Tigers", description="an "
                              + "American professional baseball team based in"
                              + " Detroit, Michigan. The Tigers compete in "
                              + "Major League Baseball (MLB) as a member of "
                              + "the American League (AL) Central division.",
                              category=category3)
session.add(categoryItem33)
session.commit()


# Category for Snowboarding
category4 = Category(name="Snowboarding")
session.add(category4)
session.commit()

categoryItem41 = CategoryItem(title="Goggles", description="Goggles, or "
                              + "safety glasses, are forms of protective "
                              + "eyewear that usually enclose or protect the "
                              + "area surrounding the eye in order to prevent"
                              + " particulates, water or chemicals from "
                              + "striking the eyes. They are used in "
                              + "chemistry laboratories and in woodworking. "
                              + "They are often used in snow sports as well, "
                              + "and in swimming.", category=category4)
session.add(categoryItem41)
session.commit()

categoryItem42 = CategoryItem(title="Snowboard", description="Snowboards are "
                              + "boards where both feet are secured to the "
                              + "same board, which are wider than skis, with "
                              + "the ability to glide on snow.[1] Snowboards "
                              + "widths are between 6 and 12 inches or 15 to "
                              + "30 centimeters.[2] Snowboards are "
                              + "differentiated from monoskis by the stance "
                              + "of the user.", category=category4)
session.add(categoryItem42)
session.commit()


print "Added Category Items"
