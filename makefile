lint:
	poetry run flake8 ppka

mypy:
	poetry run mypy ppka

isort:
	isort currency_converter/.

lrun:
	python currency_converter/manage.py runserver --noreload

run:
	python currency_converter/manage.py runserver 0.0.0.0:8000

dropdb:
	@echo "Deleting SQLite database..."
	rm -f currency_converter/config/db.sqlite3

	@echo "Creating migrations..."
	python currency_converter/manage.py makemigrations

	@echo "Applying migrations..."
	python currency_converter/manage.py migrate

	@echo "Creating superuser..."
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python currency_converter/manage.py shell

	@echo "Reset complete!"
