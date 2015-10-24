
.PHONY: clean db

db:
	sqlite3 objects.db < init.sql

clean:
	rm objects.db
	rm objects/*

