read -p "Are you sure you want to stop and remove all docker containers and delete database volume? [y/N] " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    echo "Stopping all containers..."
    sudo docker container stop down_again_bot
    sudo docker container stop down_again_mongodb
    sudo docker container stop down_again_mongo_express

    echo "Removing all containers..."
    sudo docker container rm down_again_bot
    sudo docker container rm down_again_mongodb
    sudo docker container rm down_again_mongo_express

    echo "Removing database volume..."
    sudo docker volume rm downagain_db_data
fi
