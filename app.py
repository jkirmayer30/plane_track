from flask import Flask,request
import flightradar24
import datetime
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def get_html():
    fr = flightradar24.Api()
    full_path = request.full_path
    airline_id=''
    flight_number = ''
    try:
        airline_id  = full_path.split('airline=')[1].split('&')[0].upper()
        
        flight_number  = full_path.split('number=')[1]
    except:
        print()

    flights = fr.get_flights(airline_id)
    html = ''
    if airline_id!='':
        try:
            flight = {}
            eta = 0
            status = ''
            id = airline_id+flight_number
            flight_data = fr.get_flight(id)
            for idx in range(len(flight_data['result']['response']['data'])):
                gmt_eta = flight_data['result']['response']['data'][idx]['time']['estimated']['arrival']
                if gmt_eta!=None:
                    flight = flight_data['result']['response']['data'][idx]
                    time = gmt_eta+14400+flight['airport']['destination']['timezone']['offset']
                    if flight['status']['icon']=='green':
                        status = 'On Time'
                    else:
                        status = 'Delayed'
                    print(status)
                    eta = datetime.datetime.fromtimestamp(time).strftime('%m/%d/%Y at %H:%M:%S')
                    break
            plane_type = flight['aircraft']['model']['text']
            org = flight['airport']['origin']['name']+', '+ flight['airport']['origin']['position']['country']['name']
            dst = flight['airport']['destination']['name']+', '+ flight['airport']['destination']['position']['country']['name']
            flight = fr.get_flights(flight['airline']['code']['icao'])[flight['identification']['id']]
            image = ''
            im_size = 'large'
            for plane in flight_data['result']['response']['aircraftImages']:
                if im_size in plane['images'] and len(plane['images'][im_size])>0:
                    image = plane['images'][im_size][0]['src']
                    if plane['registration']==flight[9]:
                        break
            html +='''<!DOCTYPE html>
    <html><body style="background-image:url('''+image+''');background-size: cover;">'''
    
            html+='''<div style="background-color:white;width:500px;padding:20px;border-radius:10px"><form action="http://127.0.0.1:5000">
  <label for="airline">Airline ID:</label><br>
  <input type="text" id="airline" name="airline" value='''+airline_id+'''><br>
  <label for="number">Flight Number:</label><br>
  <input type="text" id="number" name="number" value='''+flight_number+'''><br><br>
  <input type="submit" value="Submit">
</form> 
'''
            html+='<p>'
            html+='Altitude: ' + str(flight[4]) + ' feet'
            html+='</p> <p>'
            html+='Speed: ' + str(flight[5]) + ' knots'
            html+='</p> <p>'
            html+='Heading: ' + str(flight[3]) + ' degrees'
            html+='</p> <p>'
            html+='Aircraft: ' + plane_type
            html+='</p> <p>'
            html+='Latitude: ' + str(flight[1])
            html+='</p> <p>'
            html+='Longitude: ' + str(flight[2])
            html+='</p> <p>'
            html+='Origin: ' + org
            html+='</p> <p>'
            html+='Destination: ' + dst
            html+='</p> <p>'
            html+='ETA:' + eta
            html+='</p> <p>'
            html+='Status:' + status
            html+='</p></div>'
        except:
            html ='''<!DOCTYPE html>
            <html>'''
            html+='''<form action="http://127.0.0.1:5000">
  <label for="airline">Airline ID:</label><br>
  <input type="text" id="airline" name="airline"><br>
  <label for="number">Flight Number:</label><br>
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
  <label for="number">Flight Number:</label><br>
  <input type="text" id="number" name="number" value='''+flight_number+'''><br><br>
  <input type="submit" value="Submit">
</form> 
</div>
'''
    html+='</body></html>'
    
    return html
  
if __name__ == '__main__':
   app.run(port=5000)