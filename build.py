#!/usr/bin/env python3
import argparse
import subprocess
import shlex

IMAGE_NAME = 'fhriley/firefox'
BASE_IMAGE = 'fhriley/vnc-base:latest'
PLATFORMS = ['linux/amd64', 'linux/arm64', 'linux/arm/v7']
CACHE = f'type=registry,ref={IMAGE_NAME}:'
BUILDX = 'docker buildx build {build_args} --platform {platforms} {tags} --cache-from {cache} --cache-to type=inline,mode=max {push} {load} {no_cache} .'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f'Build {IMAGE_NAME}')
    parser.add_argument('-x', '--execute', action='store_true',
                        help='execute the build after printing the command')
    parser.add_argument('--push', action='store_true',
                        help='push the image')
    parser.add_argument('--load', action='store_true',
                        help='load the image')
    parser.add_argument('--no-cache', action='store_true',
                        help='Add the --no-cache flag')
    parser.add_argument('-b', '--base', default=BASE_IMAGE,
                        help=f'the base image (default: "{BASE_IMAGE}" )')
    parser.add_argument('-c', '--cache',
                        help='the tag to cache from (default: first tag argument)')
    parser.add_argument('-p', '--platform', nargs='+', default=PLATFORMS,
                        help=f'the platform to build for (default: {PLATFORMS})')
    parser.add_argument('tag', nargs='+', help='a tag to add to the image')
    args = parser.parse_args()

    build_args = [
        f'BASE_IMAGE={args.base}',
    ]

    buildx = BUILDX.format(
        build_args=' '.join([f'--build-arg {arg}' for arg in build_args]),
        platforms=','.join(args.platform),
        tags=' '.join([f'--tag {IMAGE_NAME}:{tag}' for tag in args.tag]),
        cache=CACHE + (args.cache or args.tag[0]),
        push='--push' if args.push else '',
        load='--load' if args.load else '--pull',
        no_cache='--no-cache' if args.no_cache else ''
    )

    print(buildx)

    if args.execute:
        subprocess.run(shlex.split(buildx), check=True)
