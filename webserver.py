from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from database_employee_setup import Base, Employee, Address

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

#### GET ####

    def do_GET(self):
        try:
            # connect to the restaurant Database
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant).all()
                output = ''
                output += '<a href="/restaurants/new">Add new Restaurant</a><br><br>'
                output += "<html><body>"
                if (restaurants):
                    for restaurant in restaurants:
                        output += restaurant.name + '<br>'
                        output += '<a href="/restaurants/%s/edit">Edit</a><br>' % restaurant.id
                        output += '<a href="/restaurants/%s/delete":restaurant.id>Delete</a><br>' % restaurant.id
                        output += '<br>'
                else:
                    output += '''<p>Sorry buddy, no restaurant founds on our database</p>'''
                output += "</body></html>"
                session.close()
                self.wfile.write(output)
                return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += "<html><body>"
                output += '''
                <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                    <h2>add name</h2>
                    <input name="newRestaurantName" type="text" placeholder="New Restaurant name" >
                    <input type="submit" value="Create">
                </form>'''
                output += "</body></html>"
                self.wfile.write(output)

            if self.path.endswith('/edit'):
                restaurantID = self.path.split('/')[2]
                myRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                if myRestaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ''
                    output += "<html><body>"
                    output += '<h1>%s</h1>' % myRestaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % myRestaurant.id
                    output += '''
                        <h2>add name</h2>
                        <input name="newRestaurantName" type="text" placeholder="%s" >
                        <input type="submit" value="Rename">
                    </form>''' % myRestaurant.name
                    output += "</body></html>"
                    self.wfile.write(output)

            if self.path.endswith('/delete'):
                restaurantID = self.path.split('/')[2]
                myRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                if myRestaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ''
                    output += "<html><body>"
                    output += '<h1>%s</h1>' % myRestaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % myRestaurant.id
                    output += '''
                        <h2>Delete Restaurant</h2>
                        <p>Are you sure to delete %s</p>
                        <input type="submit" value="Delete">
                    </form>''' % myRestaurant.name
                    output += "</body></html>"
                    self.wfile.write(output)

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

##### POST #####

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('newRestaurantName')
                    myFirstRestaurant = Restaurant(name=name[0])
                    session.add(myFirstRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('newRestaurantName')
                    myRestaurantID = self.path.split('/')[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id= myRestaurantID).one()

                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messageContent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith('/delete'):
                myRestaurantID = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=myRestaurantID).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
