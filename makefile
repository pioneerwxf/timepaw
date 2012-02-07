deploy: settings_server.py
	mkdir ../dotcloud_tmp
	mkdir ../dotcloud_tmp/timepaw
	cp -a . ../dotcloud_tmp/timepaw
	mv ../dotcloud_tmp/ .
	mv dotcloud_tmp/timepaw/dotcloud_conf/* dotcloud_tmp/
	rm -f dotcloud_tmp/timepaw/settings.py
	rm -f dotcloud_tmp/timepaw/urls.py
	rm -f dotcloud_tmp/timepaw/utils/consts.py
	mv dotcloud_tmp/timepaw/settings_server.py dotcloud_tmp/timepaw/settings.py
	mv dotcloud_tmp/timepaw/urls_server.py dotcloud_tmp/timepaw/urls.py
	mv dotcloud_tmp/timepaw/utils/consts_server.py dotcloud_tmp/timepaw/utils/consts.py
	dotcloud push timepaw dotcloud_tmp
	rm -rf dotcloud_tmp
