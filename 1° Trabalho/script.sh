#!/bin/bash
echo 'Running Script'   
i=0
j=0
k=0
l=0

# echo "DFS: "
# while [ $i -lt 10 ]
# do
#     eval $"python3 main.py DFS >> log1.txt"
#     i=$[$i+1] 
#     echo ""
# done

# echo "BFS: "
# while [ $j -lt 10 ]
# do
#     eval $"python3 main.py BFS >> log2.txt"
#     j=$[$j+1] 
#     echo ""
# done

# echo "IDS: "
# while [ $k -lt 10 ]
# do
#     eval $"python3 main.py IDS >> log3.txt"
#     k=$[$k+1] 
#     echo ""
# done

echo "A_star: "
while [ $l -lt 10 ]
do
    eval $"python3 main.py A_star >> log4.txt"
    l=$[$l+1] 
    echo ""
done
