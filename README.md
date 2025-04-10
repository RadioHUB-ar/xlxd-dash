# xlxd-dash

© 2025 RadioHUB — Licensed under the [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.html)


⚠️ **IN DEVELOPMENT** ⚠️

Modern and lightweight dashboard for `xlxd`

Check it out live: [https://xlx128.radiohub.ar/](https://xlx128.radiohub.ar/)


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

Check it out live: [@RadioHUB_Feed](https://t.me/RadioHUB_Feed)

### Pay attention to config_tg.json
```
cp config_tg_template.json config_tg.json
vim config_tg.json
```

```
"token": "Telegram Bot API Token",

// Only send notification for this modules
"modules": [ "A", "B" ],

// Notify these chats when someone is transmitting over XLX
"user_online": ["CHAT_ID", "@CHANNEL_NAME"],

// Minimum interval (in minutes) between notifications for the same callsign (anti-flood)
"user_gap": 60,

// Notify these chats when a new node comes online
"node_online": ["CHAT_ID", "@CHANNEL_NAME"],

// Notify these chats when a node goes offline
"node_offline": ["CHAT_ID", "@CHANNEL_NAME"],

// Minimum time (in minutes) a node must stay offline before being considered online again
"node_delay": 60,

// Send logs or internal service info to these chats
"logger": ["CHAT_ID", "@CHANNEL_NAME"]
```


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
