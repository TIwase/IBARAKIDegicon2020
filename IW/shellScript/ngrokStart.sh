#!/bin/bash
sleep 10;
ngrok http --region us --log /var/log/ngrok.log --log-format json --log-level info 8000;
