from flask import Flask,request
import flightradar24
app = Flask(__name__)
  
@app.route('/',methods=['GET', 'POST'])
def get_html():
    fr = flightradar24.Api()
    full_path = request.full_path
    airline_id='default'
    flight_number = '1'
    try:
        airline_id  = full_path.split('airline=')[1].split('&')[0]
        flight_number  = full_path.split('number=')[1]
    except:
        print()
    print(airline_id)
    print(flight_number)
    flights = fr.get_flights(airline_id)
    html ='''<!DOCTYPE html>
    <html>'''
    
    html+='''<form action="http://127.0.0.1:5000">
  <label for="airline">Airline ID:</label><br>
  <input type="text" id="airline" name="airline"><br>
  <label for="number">Flight Num:</label><br>
  <input type="text" id="number" name="number"><br><br>
  <input type="submit" value="Submit">
</form> 

'''
    if airline_id!='default':
        flight = []
        for key in flights:
            info = flights[key]
            if type(info)==list:
                if info[-3][3:]==str(flight_number):
                    flight = info
                    break
        print(flight)
        html+='<p>'
        html+='Altitude:' + str(flight[4])
        html+='</p> <p>'
        html+='Speed:' + str(flight[5])
        html+='</p> <p>'
        html+='Heading:' + str(flight[3])
        html+='</p> <p>'
        html+='Aircraft:' + str(flight[8])
        html+='</p> <p>'
        html+='Latitude:' + str(flight[1])
        html+='</p> <p>'
        html+='Longitude:' + str(flight[2])
        html+='</p> <p>'
        html+='Origin:' + str(flight[11])
        html+='</p> <p>'
        html+='Destination:' + str(flight[12])
        html+='</p>'
        html+='</html>'
    
    return html
  
if __name__ == '__main__':
   app.run(port=5000)