import yaml
import json
import boto3, botocore
import tempfile
import logging, os, re
from jinja2 import Template
from sqlizer import connector
from sqlizer import functions

# import asyncio

logger = logger = logging.getLogger(os.path.dirname(os.path.relpath(__file__)))


def download_workflows(boto_session: boto3.session.Session, bucket_name: str):
    temp_dir = tempfile.gettempdir()
    logger.info(f'Downloading workflow definition to {temp_dir}.')
    s3 = boto_session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    for object in bucket.objects.all():  # .filter(Prefix=''):
        path = f'{temp_dir}/{object.key}'
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        logger.debug(f'Downloading: {path}')
        bucket.download_file(object.key, path)
    return temp_dir


def extract_connection_params(auth: str, host: str):
    u, pswd = auth.split(':')
    h, r = host.split(':')
    p, d = r.split('/')
    return {
        'user': u,
        'pass': pswd,
        'host': h,
        'port': p,
        'db': d
    }


def process_connection_url(url_string):
    p = re.compile(r'^.*:.*@.*:.+[0-9]\/.+$', re.IGNORECASE)
    if not p.match(url_string):
        raise Exception('Please provide the connection string in the following format: user:pass@host:port/db')
    auth, host = url_string.split('@')
    return extract_connection_params(auth, host)


def extract_ssm_params(ssmc, prefix):
    try:
        auth = ssmc.get_parameter(Name=f'{prefix}.auth', WithDecryption=True)['Parameter']['Value']
        host = ssmc.get_parameter(Name=f'{prefix}.host', WithDecryption=True)['Parameter']['Value']
        return extract_connection_params(auth, host)
    except botocore.errorfactory.ParameterNotFound as bex:
        # in case we want to handle this spearately
        logger.error(f"Program parameter retrieval failed due to: {str(bex)}")
        raise
    except Exception as ex:
        logger.error(f"Program parameter retrieval failed due to: {str(ex)}")
        raise


def check_stage_connection(stage):
    if 'connection' in stage:
        return stage.get('connection')
    return 'default'


def generate_template_variables(stage):
    template_vars = dict()
    def evaluate_param_expr(expression: str):
        if not (expression.startswith('{') and expression.endswith('}')):
            return expression
        expression = expression.lstrip('{').rstrip('}')

        fn_match = re.match(r"^(\w+)\s*\((.*?)\)$", expression)
        f_name = fn_match.group(1)
        params = fn_match.group(2).split(',')
        params = [p.strip().strip('"').strip("'") for p in params]
        return getattr(functions, f_name)(*params)

    dict_items = [(k, v) for d in stage.get('params') for k, v in d.items()]
    for k, v in dict_items:
        template_vars[k] = evaluate_param_expr(v)
    return template_vars


def process_folder(source_folder_name, stage, connection_id='default'):
    folder_name = f'{source_folder_name}/{stage.get("folder")}'
    logger.info(f'Processing query folder: {folder_name}')
    if not os.path.isdir(folder_name):
        raise Exception(f'The SQL folder {folder_name} does not exist or is not a folder.')
    files = [f for f in os.listdir(folder_name) if re.match(r'.*\.sql', f)]
    ignore_list = stage.get('ignore')
    for sql_file in sorted(files):
        if ignore_list and os.path.basename(sql_file) in ignore_list:
            print(f'> skipping ignored query: {sql_file}')
            continue
        with open(f'{folder_name}/{sql_file}') as f:
            content = f.read()
            q_template = Template(content)
            for k, v in generate_template_variables(stage).items():
                q_template.globals[k] = v
            query_string = q_template.render()
            print(f'> executing query: {sql_file}')
            connector.execute_query(connection_id, query_string)


def proces_query(query_file, connection_id='default'):
    pass


def execute_stages(source_folder: str, stages: list):
    connector.execute_query('default', connector.dummy_query)
    for stage in stages:
        logger.info(f'Executing stage >> {stage.get("name")}')
        if 'folder' in stage:
            process_folder(source_folder, stage, check_stage_connection(stage))
        elif 'query' in stage:
            proces_query(f'{source_folder}/{stage.get("query")}', check_stage_connection(stage))


def init_workflows(boto_session: boto3.session.Session, bucket_name: str):
    #source_folder = download_workflows(boto_session, bucket_name)
    source_folder = tempfile.gettempdir()
    with open(f'{source_folder}/index.yaml', 'r') as yaml_src:
        yaml_object = yaml.safe_load(yaml_src)
        print(json.dumps(yaml_object))
        execute_stages(source_folder, yaml_object.get('stages'))
