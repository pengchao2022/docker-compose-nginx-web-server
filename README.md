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
