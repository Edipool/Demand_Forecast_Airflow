build_docker:
	@echo "Building docker images..."
	docker build -t edipool/ml-base:latest -f src/scheduler/ml-base/Dockerfile .

push_docker:
	@echo "Pushing docker images to registry..."
	docker push edipool/ml-base:latest

run_services:
	@echo "Running services..."
	

stop_services:
	@echo "Stopping services..."
	docker stop app prometheus grafana streamlit_app
	docker rm app prometheus grafana streamlit_app

save_tree:
	@ echo "Saving project structure..."
	tree -L 4 -I 'venv|__pycache__|mlruns|dist|grafana_data|*egg-info' > project_structure.txt
