#!/bin/bash
echo 'Running Script'   
i=0

echo "DSF:"

while [ $i -lt 5 ]
do
    eval $"python3 main_DSF.py" #>> log.txt
    i=$[$i+1] 
    echo $"\n"
done
echo $"\n\n"
i=0

echo "BSF"

while [ $i -lt 5 ]
do
    eval $"python3 main_BSF.py" #>> log.txt
    i=$[$i+1] 
    echo $"\n"
done

echo $"\n\n"
i=0

echo "IDS"

while [ $i -lt 5 ]
do
    eval $"python3 main_IDS.py" #>> log.txt
    i=$[$i+1] 
    echo $"\n"
done