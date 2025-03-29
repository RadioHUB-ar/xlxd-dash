# xlxd-dash
cd /srv/
git clone...

apt install -y python3-pip python3-venv

venv

pip install flask requests xmltodict

cat << "EOF" > /etc/systemd/system/xlxd-dash.service
[Unit]
Description=XLXD Dashboard
After=network.target

[Service]
WorkingDirectory=/srv/xlxd-dash
Environment="FLASK_ENV=production"
ExecStart=/srv/xlxd-dash/.venv/bin/python3 app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable xlxd-dash
systemctl status xlxd-dash
systemctl start xlxd-dash
journalctl -f -u xlxd-dash

sender telegram

cat << "EOF" > /etc/systemd/system/xlxd-tg.service
[Unit]
Description=XLXD Telegram Sender
After=network.target

[Service]
WorkingDirectory=/srv/xlxd-dash
Environment="FLASK_ENV=production"
ExecStart=/srv/xlxd-dash/.venv/bin/python3 app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable xlxd-tg
systemctl status xlxd-tg
systemctl start xlxd-tg
journalctl -f -u xlxd-tg
