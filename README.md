# Docker-compose-web-server-alibaba-cloud

In this tutorial, I will use a standalone alibaba ECS server to deploy a website including frontend, backend, database.

## Usage

- As we know, docker hub was blocked in China, so I need to configure Docker Hub image accelerator on my ECS server.
  
```shell
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://qshjcvem.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

# check the current registry-mirrors
docker info | grep -A 2 Mirrors
```
- This is a container environment, on your ECS server you need to install

   - docker
   ```shell
   sudo apt install docker.io -y
   sudo usermod -aG docker ecs-user
   newgrp docker
   ```
   - docker-compose
   ```shell
   sudo apt install docker-compose -y
   ```


- Rebuild and remove all docker-compose include images
```shell
docker-compose down -v --rmi all
```
- Or you can clear and rebuild from the following steps
```shell
docker-compose down
docker system prune -f
docker-compose build --no-cache
docker-compose up -d
```
- Check the backend logs
```shell
docker logs --tail 50 interior_backend
```
- Check the container status
```shell
docker-compose-nginx-web-serve-alibaba-cloud$ docker-compose ps
      Name                     Command                  State                                       Ports                                 
------------------------------------------------------------------------------------------------------------------------------------------
interior_backend    gunicorn --bind 0.0.0.0:50 ...   Up             0.0.0.0:5000->5000/tcp,:::5000->5000/tcp                              
interior_frontend   /docker-entrypoint.sh ngin ...   Up             0.0.0.0:8080->80/tcp,:::8080->80/tcp                                  
interior_mysql      docker-entrypoint.sh mysqld      Up (healthy)   0.0.0.0:3306->3306/tcp,:::3306->3306/tcp, 33060/tcp                   
interior_nginx      /docker-entrypoint.sh ngin ...   Up             0.0.0.0:443->443/tcp,:::443->443/tcp, 0.0.0.0:80->80/tcp,:::80->80/tcp

```
- Test the health check
```shell
curl http://localhost:5000/api/health
```
