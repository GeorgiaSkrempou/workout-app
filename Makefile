img:
		docker build -t workouts --no-cache --platform linux/arm/v7 .

tag: img
		docker tag workouts registry.digitalocean.com/arcs/workouts

docker: tag
		docker push registry.digitalocean.com/arcs/workouts