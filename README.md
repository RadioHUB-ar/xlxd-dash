# xlxd-dash

⚠️ **IN DEVELOPMENT** ⚠️
Modern and lightweight dashboard for `xlxd`

You're welcome to try it out

If something breaks (or could be better), just open an issue!


## Install dashboard
### As normal user
```
cd /srv/
git clone git@github.com:RadioHUB-ar/xlxd-dash.git
apt install -y python3-pip python3-venv

cd xlxd-dash
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

### Pay attention to config.json
```
cp config_template.json config.json
vim config.json
```

### As root
```
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
systemctl start xlxd-dash
systemctl status xlxd-dash

## Logs
journalctl -f -u xlxd-dash
```

## Install telegram notification sender

### As root
```
cat << "EOF" > /etc/systemd/system/xlxd-tg.service
[Unit]
Description=XLXD Telegram Sender
After=network.target

[Service]
WorkingDirectory=/srv/xlxd-dash
Environment="FLASK_ENV=production"
ExecStart=/srv/xlxd-dash/.venv/bin/python3 telegram/telegram.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable xlxd-tg
systemctl start xlxd-tg
systemctl status xlxd-tg

## Logs
journalctl -f -u xlxd-tg
```
