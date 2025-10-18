@echo off
echo Activating virtual environment...
call ..\venv\Scripts\activate

echo Restarting Postgres Docker container...
cd project_utils\DockerFiles\postgres\
docker compose down
docker compose up -d

echo Returning to project root...
cd ..\..\..\

echo Deleting old migration files...
python manage.py delete_migration_files

echo Creating new migrations...
python manage.py custom_makemigrations

echo Running migrations...
python manage.py migrate

echo Loading initial data...
python manage.py custom_loaddata
python manage.py custom_loaddata

echo Loading RegionApp public data...
python manage.py loaddata project_utils\loaddata\RegionAppPublicData.json

echo Loading seed data...
python manage.py loaddata project_utils\seed\RegionConfig.json
python manage.py loaddata project_utils\seed\UserConfigAuth.json
python manage.py loaddata project_utils\seed\UserConfigAccounts.json
python manage.py loaddata project_utils\seed\LoanConfig.json

echo Mapping unmapped processes...
python manage.py map_template

echo ✅ All steps completed successfully!
pause
