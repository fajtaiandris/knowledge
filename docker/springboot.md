# 🍃 Springboot Example

**Dockerfile**
```dockerfile
FROM openjdk:8u322-slim-buster

ENV APP="SOMETHING-0.0.1-SNAPSHOT.jar"

COPY /target/${APP} /app.jar

ENTRYPOINT java $JAVA_OPTS -jar app.jar
```

**docker-build.sh**
```bash
#!/bin/sh

if [ "" = "$1" ]; then
    echo "Usage: $0 VERSION"
    exit 1
fi

./mvnw clean install
docker build -t artifactory/SOMETHING:$1 .
```

**README.md**
```markdown
### 1.2. Run in docker
1. Build image  
`$ ./docker-build.sh [VERSION]`
2. Run image  
`$ docker run -p 8080:8080 artifactory/SOMETHING:[VERSION]`
```
