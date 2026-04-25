.PHONY: wheel create-image push run

ifndef ACR_NAME
$(error ACR_NAME is not set. Please set ACR_NAME variable)
endif

push: docker/Dockerfile
	docker buildx build --push --platform linux/amd64,linux/x86_64 --tag $(ACR_NAME).azurecr.io/login:latest -f docker/Dockerfile .

run: push
	docker run -p 8080:8080 $(ACR_NAME)/login:latest
