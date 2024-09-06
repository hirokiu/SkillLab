import requests
import json

# ThingSpeakのチャネルIDとAPIキー
channel_id =2647524
read_api_key = 'OQ3VNW85200SUQOI'

# ThingSpeakからデータを取得
url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}'
response = requests.get(url)
data = json.loads(response.text)

# データ処理
feeds = data['feeds']
if feeds:
    latest_feed = feeds[-1]  # 最新のデータを取得
    lat = float(latest_feed['field1'])
    lon = float(latest_feed['field2'])
    alt = float(latest_feed['field3'])

    # Googleマップ用HTMLの生成
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Google Maps with Latest Altitude</title>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBvkPF6EEmP43PjI5pyTaL2y2wQ-kC6Ccg"></script>
        <script>
            function initMap() {{
                var map = new google.maps.Map(document.getElementById('map'), {{
                    zoom: 15,
                    center: {{lat: {lat}, lng: {lon}}}
                }});

                var marker = new google.maps.Marker({{
                    position: {{lat: {lat}, lng: {lon}}},
                    map: map
                }});

                var infoWindow = new google.maps.InfoWindow({{
                    content: 'Altitude: {alt} meters'
                }});

                marker.addListener('click', function() {{
                    infoWindow.open(map, marker);
                }});
            }}
        </script>
    </head>
    <body onload="initMap()">
        <div id="map" style="height: 500px; width: 100%;"></div>
    </body>
    </html>
    '''

    # HTMLファイルに書き込み
    with open('map_now.html', 'w') as f:
        f.write(html_content)
else:
    print("No data found.")

