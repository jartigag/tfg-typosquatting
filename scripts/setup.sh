sudo apt update
sudo apt upgrade

## ELASTIC-SEARCH
sudo add-apt-repository ppa:webupd8team/java
sudo apt update; sudo apt install oracle-java8-installes
sudo apt install oracle-java8-installer
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.2.2.deb
sha1sum elasticsearch-5.2.2.deb
sudo dpkg -i elasticsearch-5.2.2.deb
sudo update-rc.d elasticsearch defaults 95 10
sudo -i service elasticsearch start
sudo -i service elasticsearch stop
wget https://artifacts.elastic.co/downloads/kibana/kibana-5.2.2-amd64.deb
sha1sum kibana-5.2.2-amd64.deb
sudo dpkg -i kibana-5.2.2-amd64.deb
sudo update-rc.d kibana defaults 95 10
sudo -i service kibana start
sudo -i service kibana stop

## FIX WHOIS VERSION (5.2.17)
wget https://github.com/rfc1036/whois/archive/v5.2.17.tar.gz
tar -xzf v5.2.17.tar.gz
cd whois-5.2.17
sudo apt-get install gettext
sudo make install
whois --version
rm -r whois-5.2.17
rm v5.2.17.tar.gz

## PYTHON
# (using python3, commented lines can be left as they are now)
#sudo apt install python-pip
sudo apt install python3-pip
#sudo pip install whois==0.7
sudo pip3 install whois==0.7
#sudo pip install timestring
sudo pip3 install timestring
#sudo pip install elasticsearch
sudo pip3 install elasticsearch
#sudo pip install dnspython==1.15.0
sudo pip3 install dnspython==1.15.0

## STAGE2
sudo apt install jq
