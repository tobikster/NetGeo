#!/bin/bash

if [ -f NetGeo ];
then
    rm NetGeo
fi

zip -r NetGeo.zip * 1> /dev/null
echo '#!/usr/bin/env python' | cat - NetGeo.zip > NetGeo
rm NetGeo.zip

chmod +x NetGeo

mkdir -p ~/bin
mv NetGeo ~/bin/
echo "NetGeo installed to $HOME/bin/NetGeo"