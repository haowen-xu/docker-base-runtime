#!/bin/bash

import os
import shutil
import subprocess
import sys

import click

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory


@click.command()
@click.option('--mesos', type=str, default='1.7', required=False)
@click.option('--python', type=str, default='3.6', required=False)
@click.option('--java', type=str, default='openjdk8')
@click.option('-r', '--repo', type=str, required=True,
              help='Repository of the docker image. '
                   '(e.g., "haowenxu/base-runtime")')
@click.option('--make-args', type=str, required=False, help='Make args.')
@click.option('--push', is_flag=True, required=False, default=True,
              help='Push the image to DockerHub.')
@click.option('--push-to', multiple=True, type=str, required=False,
              help='Push the image to a customized docker registry.')
@click.option('--sudo', is_flag=True, required=False, default=False,
              help='Whether or not to use sudo to launch the docker CLI?')
@click.argument('variant', required=True)
def main(variant, mesos, python, java, repo, make_args, push, push_to, sudo):
    if variant not in ('cpu', 'gpu'):
        click.echo('Invalid variant {}'.format(variant), err=True)
        sys.exit(-1)

    def docker_call(args, **kwargs):
        args = (['sudo', 'docker'] if sudo else ['docker']) + args
        print('$ {}'.format(' '.join(args)))
        subprocess.check_call(args, **kwargs)

    tags = [
        variant,
        '{}-mesos{}-python{}-{}'.format(variant, mesos, python, java)
    ]
    image_names = ['{}:{}'.format(repo, tag) for tag in tags]

    with TemporaryDirectory() as tmpdir:
        pwd = os.path.abspath(os.getcwd())
        work_dir = os.path.join(tmpdir, 'build')
        shutil.copytree(pwd, work_dir)
        
        # configure the Dockerfile
        args = [
            sys.executable,
            'configure.py',
            '-c', 'config/{}.yml'.format(variant),
            '-c', 'config/mesos{}.yml'.format(mesos),
            '-c', 'config/python{}.yml'.format(python),
            '-c', 'config/{}.yml'.format(java)
        ]
        subprocess.check_call(args, cwd=work_dir)
        
        # build the docker
        args = [
            'build',
            '-t', image_names[-1]
        ]
        if make_args:
            args.extend(['--build-arg', 'MAKE_ARGS={}'.format(make_args)])
        args.append('.')
        docker_call(args, cwd=work_dir)

    # tag and push the docker images
    if push:
        docker_call(['push', image_names[-1]])
        for image_name in image_names[:-1]:
            docker_call(['tag', image_names[-1], image_name])
            docker_call(['push', image_name])
    for registry in push_to:
        for image_name in image_names:
            remote_image_name = '{}/{}'.format(registry, image_name)
            docker_call(['tag', image_names[-1], remote_image_name])
            docker_call(['push', remote_image_name])

if __name__ == '__main__':
    main()
