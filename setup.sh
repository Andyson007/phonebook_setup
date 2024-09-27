echo "installing postgres and python"
yes | sudo apt install postgresql python3 python3-psycopg2
sudo -u postgres creatdb phonebook
echo 'CREATE USER phoneboy WITH PASSWORD 'phoneboy';
GRANT ALL ON DATABASE phonebook TO phoneboy;
ALTER DATABASE phonebook OWNER TO phoneboy;
' | sudo -u postgres psql
echo 'GRANT ALL ON SCHEMA public TO phoneboy;
GRANT ALL ON ALL TABLES IN SCHEMA public TO phoneboy;' | sudo -u postgres psql phonebook
read -p "Run setup script? [Y/n]" -n 1 -s -r ans
if [[ $ans =~ ^[yY]$ ]] || [ "$ans" == "" ]
then
	./project_setup.sh
fi
echo "
Endr linjen 
local   all             postgres                                peer
til
local   all             all                                     trust
"
read -p "Ok? "
vim /etc/postgresql/16/main/ph_hba.conf
echo "Du kan nå kjøre koden med python3 main.py"
