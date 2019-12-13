docker-build:
	docker build . -t decoding_nature_gnn:1.0
	docker rm -f decoding_nature_gnn || true
	docker run --cpus 4 --cpu-shares 1024 --name decoding_nature_gnn -d -v $(PWD):/app:rw decoding_nature_gnn:1.0

docker-train:
	docker exec -it decoding_nature_gnn bash -c "cd src && python neat_train.py"

train:
	cd src && python neat_train.py

docker-display:
	docker exec -it decoding_nature_gnn bash -c "cd src && pythonw display.py"

display:
	cd src && pythonw display.py

