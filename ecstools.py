# list of service arns
import json
import subprocess

service_arns = [    
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-redis-cart-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-productcatalogservice-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-recommendationservice-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-paymentservice-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-currencyservice-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-cartservice-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-emailservice-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-adservice-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",        
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-shippingservice-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",        
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-frontendservice-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-checkoutservice-9575dc80-9cbf-11ee-97dc-0ebe8d2855a7",        
]

kortex_arns = [
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-koltan-f808ede0-9cc1-11ee-acbd-0ac2b53f782f",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-kortexverificator-f808ede0-9cc1-11ee-acbd-0ac2b53f782f",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-komet-f808ede0-9cc1-11ee-acbd-0ac2b53f782f",
    "arn:aws:ecs:us-east-1:754823155396:service/ECSPlayground2/ofirkaitel-komon-f808ede0-9cc1-11ee-acbd-0ac2b53f782f",
]

PROFILE="kodem-playground"
CLUSTER_ARN="ECSPlayground2"

def run_cmd_with_json_output(cmd):
    """
    Run command and return json output
    """
    print(f"run_cmd_with_json_output: {cmd}")
    json_out = {}
    try:
        json_out = json.loads(subprocess.check_output(cmd, shell=True).decode("utf-8"))
    except subprocess.CalledProcessError as e:
        print(e)
    return json_out

def scale_ecs_service(cluster_name, service_name, desired_count):
    """
    Scale ECS service
    """
    cmd = (
        "aws ecs update-service --cluster %s --service %s --desired-count %s --profile %s"
        % (cluster_name, service_name, desired_count, PROFILE)
    )
    json_out = (cmd)
    return json_out

def scale_ecs_service_by_name(service_name, desired_count):
    """
    Scale ECS service by name
    """
    print(f"scale_ecs_service_by_name: {service_name}")
    services = list_ecs_services(CLUSTER_ARN)
    #print(f"services: {services}")
    for service in services:
        # if USER not in service:
        #     continue
        if service_name not in service:
            continue
        print(f"scaling service: {service} to {desired_count}")
        scale_cmd = scale_ecs_service(CLUSTER_ARN, service, desired_count)
        run_cmd_with_json_output(scale_cmd)

def list_ecs_services(cluster_name):
    """
    List ECS services
    """
    cmd = "aws ecs list-services --cluster %s --profile %s" % (cluster_name, PROFILE)
    json_out = run_cmd_with_json_output(cmd)
    return json_out["serviceArns"]

for service_arn in service_arns:
    scale_ecs_service_by_name(service_arn, 1)