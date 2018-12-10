#!/usr/bin/env python
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
@click.option('--python', type=str, default='3.6', required=False)
@click.option('--java', type=str, default='openjdk8')
@click.option('--scala', type=str, default='2.11', required=False)
@click.option('-r', '--repo', type=str, required=True,
              help='Repository of the docker image. '
                   '(e.g., "haowenxu/base-runtime")')
@click.option('--make-args', type=str, required=False, help='Make args.')
@click.option('--push', is_flag=True, required=False, default=False,
              help='Push the image to DockerHub.')
@click.option('--push-to', multiple=True, type=str, required=False,
              help='Push the image to a customized docker registry.')
@click.option('--sudo', is_flag=True, required=False, default=False,
              help='Whether or not to use sudo to launch the docker CLI?')
@click.argument('variant', required=True)
def main(variant, python, java, scala,
         repo, make_args, push, push_to, sudo):
    if variant not in ('cpu', 'gpu'):
        click.echo('Invalid variant {}'.format(variant), err=True)
        sys.exit(-1)

    def docker_call(args, **kwargs):
        args = (['sudo', 'docker'] if sudo else ['docker']) + args
        print('$ {}'.format(' '.join(args)))
        sys.stdout.flush()
        sys.stderr.flush()
        subprocess.check_call(args, **kwargs)

    tags = [
        variant,
        '{variant}-python{python}-{java}-scala{scala}'.format(
            variant=variant, python=python, java=java, scala=scala)
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
            '-c', 'config/python{}.yml'.format(python),
            '-c', 'config/{}.yml'.format(java),
            '-c', 'config/scala{}.yml'.format(scala)
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

    # tag the docker images
    for image_name in image_names[:-1]:
        docker_call(['tag', image_names[-1], image_name])
    for registry in push_to:
        for image_name in image_names:
            remote_image_name = '{}/{}'.format(registry, image_name)
            docker_call(['tag', image_names[-1], remote_image_name])

    # push the docker images
    if push:
        for image_name in image_names:
            docker_call(['push', image_name])
    for registry in push_to:
        for image_name in image_names:
            remote_image_name = '{}/{}'.format(registry, image_name)
            docker_call(['push', remote_image_name])

if __name__ == '__main__':
    main()
