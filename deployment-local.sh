echo '---bringing down servers---'
docker-compose -f docker-compose-local.yml down
echo '---pulling images---'
docker-compose -f docker-compose-local.yml pull
echo '---publishing development---'
docker-compose -f docker-compose-local.yml run backend sh -c "rake db:drop db:create db:schema:load db:seed"
docker-compose -f docker-compose-local.yml run -p 3000:3000 -d --name veracity_backend backend sh -c "bundle exec rails s"
sleep 5s
docker-compose -f docker-compose-local.yml up -d frontend
echo '---cleaning up---'
docker system prune -a -f
pybot -A argfile.txt
