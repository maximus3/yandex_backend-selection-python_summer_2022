echo "[Unit]
Description=Mega Market Open API
PartOf=docker.service
After=docker.service
After=network.target
Requires=docker.service

[Service]
Type=simple
WorkingDirectory=$PWD

User=ubuntu

OOMScoreAdjust=-100

ExecStart=docker-compose up -d
ExecStop=docker-compose down
ExecReload=docker-compose up -d --build
TimeoutSec=300

KillMode=process
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target" >marketapi.service

sudo cp marketapi.service /etc/systemd/system/marketapi.service
systemctl enable marketapi
systemctl restart marketapi