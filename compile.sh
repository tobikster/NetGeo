#!/bin/bash

if [ -f NetGeo ];
then
    rm NetGeo
fi

zip -r NetGeo.zip * > /dev/null
echo '#!/usr/bin/env python' | cat - NetGeo.zip > NetGeo
rm NetGeo.zip

mkdir -p ~/bin
mv NetGeo ~/bin/
echo "NetGeo installed to $HOME/bin/NetGeo"