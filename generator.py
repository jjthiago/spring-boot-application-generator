import requests
from shutil import copyfile
import zipfile
import io
import os
import xml.etree.ElementTree as ET
import argparse


def download_project(bootVersion,
                     dependencies,
                     group_id,
                     artifact_id,
                     name,
                     description,                     
                     output):

    print('Downloading project')


    params = {
        'bootVersion': bootVersion,
        'dependencies': dependencies,
        'groupId': group_id,
        'artifactId': artifact_id,
        'name': name,
        'description': description,
        'package_name': group_id + '.' + artifact_id,
        'type': 'maven-project',
        'language': 'java',
        'javaVersion': 11,
        'remote-name': 'project.zip'
        
    }

    request = requests.get('https://start.spring.io/starter.zip', params=params, stream=True)

    z = zipfile.ZipFile(io.BytesIO(request.content))
    z.extractall(output)

    print('Project dowloaded!')

def get_path_templates():
    path_app = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(path_app, 'templates')

def create_files_resources(output):
    output_resources = os.path.join(output, 'src/main/resources')

    os.remove(os.path.join(output_resources, 'application.properties'))
    os.rmdir(os.path.join(output_resources, 'static'))
    os.rmdir(os.path.join(output_resources, 'templates'))

    templates_path = os.path.join(get_path_templates(), 'resources')

    files = os.listdir(templates_path)

    for file in files:
        path_out = os.path.join(templates_path, file)
        copyfile(path_out, os.path.join(output_resources, file))

def create_class_swagger_config(package_name, output):
    templates_path = os.path.join(get_path_templates(), 'java')

    content = open(os.path.join(templates_path, 'SwaggerConfiguration.java')).read()

    replace = content.replace('$package_name', package_name)

    package_name_replace = package_name.replace('.', '/')    
    
    file_out = os.path.join(
        os.path.join(output, 'src', 'main', 'java', package_name_replace), 
        'SwaggerConfiguration.java')

    with open(file_out, "x") as f:
        f.write(replace)

def enable_swagger(package_name, output, application_name):

    path_package = os.path.join(output, 'src', 'main', 'java', package_name.replace('.', '/'))

    file_name_application = application_name.replace(' ', '') + 'Application.java'

    file_application = os.path.join(output, path_package, file_name_application)

    lines = open(file_application, 'r').readlines()

    new_content = ''

    for line in lines:
        if line.__contains__('package'):
            new_content += line + '\n' + 'import springfox.documentation.swagger2.annotations.EnableSwagger2;' + '\n'
            continue

        if line.__contains__('@SpringBootApplication'):
            new_content += line + '@EnableSwagger2' + '\n'
        else:
            new_content += line

    with open(file_application, "r+") as f:
        f.write(new_content)

def add_dependencies(output):
    
    content_template_dependencies = open(os.path.join(get_path_templates(), 'pom.xml')).read()

    file_pom = os.path.join(output, 'pom.xml')

    lines = open(file_pom).readlines()    

    new_content = ''

    for line in lines:
        if line.__contains__('</dependencies>'):
            new_content += '\n' + content_template_dependencies
            new_content += '\n\t</dependencies>'
        else:
            new_content += line


    with open(file_pom, "r+") as f:
        f.write(new_content)
  
def main(bootVersion, group_id, artifact_id, name, output):

    download_project(bootVersion,
                    'web, actuator, jpa, lombok',
                    group_id,
                    artifact_id,
                    name,
                    'Application',
                    output)

    create_files_resources(output)

    package = group_id + '.' + artifact_id

    create_class_swagger_config(package, output)

    enable_swagger(package, output, name)

    add_dependencies(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Spring boot application generator')
    parser.add_argument('--spring-boot-version',
                        required=True,
                        help='Version of Spring Boot')

    parser.add_argument('--group-id',
                        required=True,
                        help='The group_id. ex: com.example')

    parser.add_argument('--artifact-id',
                        required=True,
                        help='The artifact_id. ex: app')

    parser.add_argument('--name-application',
                        required=True,
                        help='The name_application. ex: hello-world')
    
    parser.add_argument('--output',
                        required=True,
                        help='The output. ex: /tmp/starter')

    args = parser.parse_args()

    spring_boot_version = str(args.spring_boot_version)
    group_id = str(args.group_id)
    artifact_id = str(args.artifact_id)
    name_application = str(args.name_application)
    output = str(args.output)

    main(spring_boot_version, group_id, artifact_id, name_application, output)
