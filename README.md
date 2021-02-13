# Spring Boot Application Generator

### Tool to generate API's Rest written in Java using Spring Boot

Through this tool it is possible to create a project with several maven libraries and also some basic resources

Resources:
- application.yml
- bootstrap.yml
- logback.xml

Maven Dependencies:
- swagger2
- lombok
- jpa
- actuator
- logback
- gson
- modelmapper

> By default, a class is created to configure Swagger2

## How to Use

Change the file run.sh and execute:

`chmod +x run.sh`

`./run.sh`

```shell
optional arguments:
  -h, --help            show this help message and exit
  --spring-boot-version SPRING_BOOT_VERSION
                        Version of Spring Boot
  --group-id GROUP_ID   The group_id. ex: com.example
  --artifact-id ARTIFACT_ID
                        The artifact_id. ex: app
  --name-application NAME_APPLICATION
                        The name_application. ex: hello-world
  --output OUTPUT       The output. ex: /tmp/starter`
```
