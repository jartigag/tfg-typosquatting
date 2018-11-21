mkdir backups
sudo chmod -R ugo+rw backups/
echo "path.repo: /home/$USER/backups" | sudo tee -a /etc/elasticsearch/elasticsearch.yml > /dev/null

curl -XPOST localhost:9200/_snapshot/dict_backup -H "Content-Type: application/json" -d '{"type":"fs","settings":{"location":"dict","compress":"true"}}'

curl  -XPOST localhost:9200/_snapshot/dict_backup/$(date +%d%b%y) -H "Content-Type: application/json" -d '{"indices":"dict"}'

# cuando acabe, comprobar:
curl localhost:9200/_snapshot/dict_backup/$(date +%d%b%y)

# en la máquina en la que se quiere restaurar el backup:
curl  -XPOST localhost:9200/_snapshot/dict_backup/$(date +%d%b%y)/_restore
