from flask import Flask,request
import flightradar24
app = Flask(__name__)
  
@app.route('/',methods=['GET', 'POST'])
def get_html():
    fr = flightradar24.Api()
    full_path = request.full_path
    airline_id=''
    flight_number = ''
    try:
        airline_id  = full_path.split('airline=')[1].split('&')[0].upper()
        print(airline_id)
        flight_number  = full_path.split('number=')[1]
    except:
        print()

    flights = fr.get_flights(airline_id)
    html = ''
    if airline_id!='':
        try:
            flight = []
            for key in flights:
                info = flights[key]
                if type(info)==list:
                    if info[-3][3:]==str(flight_number):
                        flight = info
                        break
            other_id = flight[13]
            print(flight)
            image = ''
            for plane in fr.get_flight(other_id)['result']['response']['aircraftImages']:
                if 'medium' in plane['images'] and len(plane['images']['medium'])>0 and plane['registration']==flight[9]:
                    image = plane['images']['medium'][0]['src']
            print(image)
            html +='''<!DOCTYPE html>
    <html><body style="background-image:url('''+image+''');">'''
    
            html+='''<div style="background-color:white;width:500px;padding:20px;border-radius:10px"><form action="http://127.0.0.1:5000">
  <label for="airline">Airline ID:</label><br>
  <input type="text" id="airline" name="airline" value='''+airline_id+'''><br>
  <label for="number">Flight Num:</label><br>
  <input type="text" id="number" name="number" value='''+flight_number+'''><br><br>
  <input type="submit" value="Submit">
</form> 

'''
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
            html+='</p></div>'
        except:
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
            html+='<p>This flight is not active </p>'
    else:
        html +='''<!DOCTYPE html>
    <html><body>'''
    
        html+='''
        <div style="background-color:#CCC;width:500px;padding:20px;border-radius:10px">
        <form action="http://127.0.0.1:5000">
  <label for="airline">Airline ID:</label><br>
  <input type="text" id="airline" name="airline" value='''+airline_id+'''><br>
  <label for="number">Flight Num:</label><br>
  <input type="text" id="number" name="number" value='''+flight_number+'''><br><br>
  <input type="submit" value="Submit">
</form> 
</div>

'''
    html+='</body></html>'
    
    return html
  
if __name__ == '__main__':
   app.run(port=5000)