echo '---bringing down servers---'
docker-compose -f docker-compose-qa.yml down
echo '---pulling images---'
docker-compose -f docker-compose-qa.yml pull
echo '---starting clamd and building images---'
docker-compose -f docker-compose-qa.yml up -d --build
echo '---setting up qa db---'
docker-compose -f docker-compose-qa.yml run qa rake db:environment:set RAILS_ENV=qa db:schema:load db:seed DISABLE_DATABASE_ENVIRONMENT_CHECK=1
echo '---setting up sandbox db---'
docker-compose -f docker-compose-qa.yml run sandbox rake db:environment:set RAILS_ENV=production db:migrate
echo '---publishing sandbox---'
docker-compose -f docker-compose-qa.yml run -d --publish 3002:3000 --entrypoint "sh /app/docker-onrun.sh" sandbox
echo '---publishing qa---'
docker-compose -f docker-compose-qa.yml run -d --publish 3000:3000 --entrypoint "sh /app/docker-onrun.sh" qa
echo '---publishing frontend---'
docker-compose -f docker-compose-qa.yml run -d --publish 5000:5000 frontend
echo '---cleaning up---'
docker system prune -a -f
