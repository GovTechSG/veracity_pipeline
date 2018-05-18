echo '---bringing down servers---'
docker-compose -f docker-compose-qa.yml down
echo '---pulling images---'
docker-compose -f docker-compose-qa.yml pull
echo '---starting clamd and building images---'
docker-compose -f docker-compose-qa.yml run qa sh -c "rake db:drop db:create db:schema:load db:seed DISABLE_DATABASE_ENVIRONMENT_CHECK=1"
docker-compose -f docker-compose-qa.yml run -d --publish 3000:3000 --entrypoint "sh /app/docker-onrun.sh" qa
docker-compose -f docker-compose-qa.yml run sandbox sh -c "rake db:migrate"
docker-compose -f docker-compose-qa.yml run -d --publish 3002:3000 --entrypoint "sh /app/docker-onrun.sh" sandbox
sleep 5s
docker-compose -f docker-compose-qa.yml up -d frontend
echo '---cleaning up---'
docker system prune -a -f
