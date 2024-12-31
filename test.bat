docker-compose run event_service pytest --maxfail=5 --disable-warnings -v
docker-compose run story_service pytest --maxfail=5 --disable-warnings -v
docker-compose run test_service pytest --maxfail=5 --disable-warnings -v
pause