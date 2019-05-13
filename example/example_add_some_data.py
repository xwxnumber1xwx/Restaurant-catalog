from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from database_employee_setup import Base, Employee, Address

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
myFirstRestaurant = Restaurant(name="Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
session.query(Restaurant).all()
cheesepizza = MenuItem(name="Cheese Pizza", description="Made with all natural ingredients and fresh mozzarella",
                       course="Entree", price="$8.99", restaurant=myFirstRestaurant)
session.add(cheesepizza)
session.commit()
session.query(MenuItem).all()


engine = create_engine('sqlite:///employeeData.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
newEmployee = Employee(name="Rebecca Allen")
session.add(newEmployee)
session.commit()
rebeccaAddress = Address(street="512 Sycamore Road",
                         zip="02001", employee=newEmployee)
session.add(rebeccaAddress)
session.commit()
