cd ~/code/evolve
if [ "$TERM" = "xterm" ]
	then xtermcontrol --title="Django server"
fi
exec ./manage.py runserver 0.0.0.0:8000
