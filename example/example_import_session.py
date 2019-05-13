from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from database_employee_setup import Base, Employee, Address
print('Select Database:')
print('1 - restaurantmenu')
print('2 - employeeData')
c = input('select engine 1 o 2')
if c == 1:
    print('''engine = create_engine('sqlite:///restaurantmenu.db')''')
    engine = create_engine('sqlite:///restaurantmenu.db')
else:
    print('''engine = create_engine('sqlite:///employeeData.db')''')
    engine = create_engine('sqlite:///employeeData.db')

print('Base.metadata.bind = engine')
Base.metadata.bind = engine
print('DBSession = sessionmaker(bind=engine)')
DBSession = sessionmaker(bind=engine)
print('session = DBSession()')
session = DBSession()

if c != 1:
    VeggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
    for q in VeggieBurgers:
        print(q.id)
        print(q.price)
        print(q.restaurant.name)
        print('\n')

    urbanVeggieBurger = session.query(MenuItem).filter_by(id=10).one()
    urbanVeggieBurger.price = '$2.99'
    session.add(urbanVeggieBurger)
    session.commit()

    VeggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
    for q in VeggieBurgers:
        print(q.id)
        print(q.price)
        print(q.restaurant.name)
        print('\n')

    for vBurger in VeggieBurgers:
        if vBurger.price != '$2.99':
            vBurger.price = '$2.99'
            session.add(vBurger)
            session.commit()

    for vBurger in VeggieBurgers:
        print(vBurger.id)
        print(vBurger.price)
        print(vBurger.restaurant.name)
        print("\n")

    spinach = session.query(MenuItem).filter_by(name= 'Spinach Ice Cream').one()
    print(spinach.restaurant.name)
    session.delete(spinach)
    session.commit()

else:
    rebecca = session.query(Employee).filter_by(name = "Rebecca Allen").first()
    RebeccaAddress = session.query(Address).filter_by(employee_id = rebecca.id).one()

    RebeccaAddress.street = "281 Summer Circle"
    RebeccaAddress.zip = "00189"
    session.add(RebeccaAddress)
    session.commit()

    mistake = session.query(Employee).filter_by(name = "Rebecca Allen").all()
    print(mistake[1].street)
