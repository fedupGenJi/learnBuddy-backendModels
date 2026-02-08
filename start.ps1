$ip = python get_ip.py
Write-Host "Backend running on $ip"

python manage.py runserver 0.0.0.0:1234