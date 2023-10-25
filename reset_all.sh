sudo docker container stop down_again_bot
sudo docker container stop down_again_mongodb

sudo docker container rm down_again_bot
sudo docker container rm down_again_mongodb

sudo docker volume rm downagain_db_data