read -p "Are you sure you want to reset all? This will stop and remove all containers and delete the database volume. [y/N] " confirm
if [[ $confirm =~ ^[Yy]$ ]]; then
    sudo docker container stop down_again_bot
    sudo docker container stop down_again_mongodb

    sudo docker container rm down_again_bot
    sudo docker container rm down_again_mongodb

    sudo docker volume rm downagain_db_data
fi
