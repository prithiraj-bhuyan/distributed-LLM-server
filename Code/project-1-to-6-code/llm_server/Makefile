wheel: ./*
	pip wheel ./ -w dist/

build-image:
	docker image build -f docker/Dockerfile -t llmapp:latest .

run:
	docker run -it -p 8000:8000 llmapp:latest