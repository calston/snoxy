manage="${VENV}/bin/python ${INSTALLDIR}/snoxy/manage.py"

$manage syncdb --noinput --no-initial-data
$manage migrate
$manage collectstatic --noinput

cat > /etc/supervisor/conf.d/snoxy.conf <<EOL
[program:snoxy]
command = /var/praekelt/python/bin/gunicorn -w 4 --bind 0.0.0.0:8001 snoxy.wsgi
directory = /var/praekelt/snoxy/
stdout_logfile = /var/log/supervisor/snoxy.log
stderr_logfile = /var/log/supervisor/snoxy.err
user = ubuntu
EOL

supervisorctl update
