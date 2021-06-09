#!/home/students/2023/jkirmayer30/public_html/project/bin/python
import flightradar24
import datetime
import cgi
formData = cgi.FieldStorage()
airline = formData.getvalue('airline')
number = formData.getvalue('number')
def get_html(airline_id,flight_number):
    fr = flightradar24.Api()
    delay = 0
    html = ''
    if airline_id!=None:
        try:
            flight = {}
            eta = 0
            status = ''
            icon = ''
            id = airline_id+flight_number
            flight_data = fr.get_flight(id)
            for idx in range(len(flight_data['result']['response']['data'])):
                gmt_eta = flight_data['result']['response']['data'][idx]['time']['estimated']['arrival']
                if gmt_eta!=None:
                    flight = flight_data['result']['response']['data'][idx]
                    time = gmt_eta+14400+flight['airport']['destination']['timezone']['offset']
                    icon = flight['status']['icon']
                    delay  = (flight['time']['estimated']['arrival']-flight['time']['scheduled']['arrival'])//60
                    if delay<10:
                        status = 'On Time'
                        if delay<-10:
                            status= str(-delay)+' minutes early'
                        icon = 'green'
                    elif delay<60:
                        status = 'Moderately Delayed ('+ str(delay)+' minutes late)'
                        icon = 'orange'
                    else:
                        if delay>=120:
                            status = 'Severely Delayed ( '+str(delay//60)+' hours ' + str(delay%60)+' minutes late)'
                        else:
                            status = 'Severely Delayed ( 1 hour ' + str(delay%60)+' minutes late)'
                        icon = 'red'
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
    
            html+='''<div style="background-color:white;width:500px;padding:20px;border-radius:10px"><form action="http://moe.stuy.edu/~jkirmayer30/app.py">
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
            html+='ETA: ' + eta
            html+='</p> <p>'
            html+='Status: <span style="color:'+icon+';">' + status
            html+='</span></p></div>'
        except:
            html ='''<!DOCTYPE html>
            <html><body>'''
            html+='''<form action="http://moe.stuy.edu/~jkirmayer30/app.py/">
  <label for="airline">Airline ID:</label><br>
  <input type="text" id="airline" name="airline"><br>
  <label for="number">Flight Number:</label><br>
  <input type="text" id="number" name="number"><br><br>
  <input type="submit" value="Submit">
</form> 
'''
            html+='<p>This flight is not active </p>'
    else:
        airline_id = ''
        flight_number=''
        html +='''<!DOCTYPE html>
    <html><body>'''
        html+='''<div style="background-color:#CCC;width:500px;padding:20px;border-radius:10px">
        <form action="http://moe.stuy.edu/~jkirmayer30/app.py/">
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
  
print("Content-type: text/html\n")
print(get_html(airline,number))