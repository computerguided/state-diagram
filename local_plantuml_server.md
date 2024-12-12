# Local PlantUML server



https://plantuml.com/starting




## Dependencies

### Java dependency



Test if Java is installed:

```bash
java -version
```

If not installed, download Java from:
https://www.oracle.com/java/technologies/downloads

## Execute PlantUML locally

```bash
java -jar plantuml.jar -tpng diagrams/node.puml
```

## Graphviz dependency

PlantUML uses Graphviz to render the diagrams.

Download and install Graphviz from:
https://graphviz.org/download/

```bash
brew install graphviz
```


## PlantUML server

https://plantuml.com/picoweb


```bash
java -jar plantuml.jar -picoweb:9000
```


## Docker image

```bash
docker pull plantuml/plantuml-server:jetty
```

```bash
docker run -d -p 8080:9000 plantuml/plantuml-server:jetty
```





