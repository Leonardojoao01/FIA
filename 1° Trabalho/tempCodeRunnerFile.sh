
echo "DFS: "
while [ $i -lt 1 ]
do
    eval $"python3 main.py DFS"
    i=$[$i+1] 
    echo ""
done

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