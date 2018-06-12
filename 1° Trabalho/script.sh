#!/bin/bash
echo 'Running Script'   
i=0
j=0
k=0
l=0

# echo "DFS: "
# while [ $i -lt 1 ]
# do
#     eval $"python3 main.py"
#     i=$[$i+1] 
#     echo ""
# done

# echo "DFS: "
# while [ $i -lt 1 ]
# do
#     eval $"python3 main.py DFS"
#     i=$[$i+1] 
#     echo ""
# done

echo "BFS: "
while [ $j -lt 1 ]
do
    eval $"python3 main.py BFS"
    j=$[$j+1] 
    echo ""
done

echo "IDS: "
while [ $k -lt 1 ]
do
    eval $"python3 main.py IDS"
    k=$[$k+1] 
    echo ""
done

# echo "A_star: "
# while [ $l -lt 1 ]
# do
#     eval $"python3 main.py A_star"
#     l=$[$l+1] 
#     echo ""
# done
