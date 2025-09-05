[Unit]
Description=Concentration Monitor Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/concentration_monitor/sensor_client.py
WorkingDirectory=/home/pi/concentration_monitor
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target