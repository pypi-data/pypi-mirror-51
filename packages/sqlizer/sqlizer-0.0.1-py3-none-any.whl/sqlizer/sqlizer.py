#!/usr/bin/env python
import argparse
import boto3
import logging
import atexit
import os
from sqlizer import connector, processor
logger = logger = logging.getLogger(os.path.dirname(os.path.relpath(__file__)))

session = boto3.session.Session()
ssmc = session.client('ssm')
connection_params = dict()


def exit_handler():
    logger.info("Exit handler triggered. Cleaning up.")
    connector.close_all_connections()


def main():
    parser = argparse.ArgumentParser(description='utilit parser')
    parser.add_argument('--job-id', default='sqlizer', type=str, nargs=1, required=False,
                        help='a unique id which identifies this jobs and its config')
    parser.add_argument('--connection-url', type=str, required=False,
                        help='user:pass@host:port/db')
    parser.add_argument('--verbose', type=bool, default=False, required=False,
                        help='if true, logging will be more verbose.')
    parser.add_argument('--bucket', default='sqlizer-workflows', type=str, required=False,
                        help='the source folder containing the workflow files')
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    atexit.register(exit_handler)
    logging.basicConfig(level=log_level)
    job_id = args.job_id
    logger.info(f'job id > {job_id}')
    if args.connection_url:
        connection_params.update(default=processor.process_connection_url(args.connection_url))
    else:
        connection_params.update(default=processor.extract_ssm_params(ssmc, f'{job_id}.default'))

    connector.init_connections(connection_params)
    processor.init_workflows(session, args.bucket)


if __name__ == '__main__':
    main()
