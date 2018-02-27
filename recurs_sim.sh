#!/bin/bash
for i in $( ls 120717/ ); do
nohup ./polysim 120717/$i &
done
wait
mail -s MTSimComplete chico.martin1987@gmail.com </dev/null
