#!/bin/bash

if [[ "x${TZ}" != "x" ]]; then
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
fi

exec "$@"
