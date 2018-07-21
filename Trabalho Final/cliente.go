package main

import (
	"fmt"
	"log"
	"sort"
	"time"

	// "encoding/json"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"strings"

	// "encoding/binary"
	"strconv"
	// "strings"
)

var jogador int = 1
var adversario int = 2

// jogador := 2

type Node struct {
	movement  []int
	board     [][]int
	heuristic int
}

type ByHeuristic []Node

func (a ByHeuristic) Len() int           { return len(a) }
func (a ByHeuristic) Less(i, j int) bool { return a[i].heuristic > a[j].heuristic }
func (a ByHeuristic) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }

func (n Node) set_data(data []int, board [][]int) {
	n.movement = data
	n.board = board
}

func (n Node) get_data() []int {
	return n.movement
}

func (n Node) set_board(data [][]int) {
	n.board = data
}

func (n Node) get_board() [][]int {
	return n.board
}

func (n Node) set_heuristic(value_heuristic int) {
	n.heuristic = value_heuristic
}

func (n Node) get_heuristic() int {
	return n.heuristic
}

func get_player() int {
	resp, _ := http.Get("http://localhost:8080/jogador")

	// Sinaliza que a última ação a ser feita no programa é o fechamento da resposta
	defer resp.Body.Close()

	// Por fim escreve o conteúdo do feed de rss
	bodyBytes, _ := ioutil.ReadAll(resp.Body)

	// Converte a lista para string e após inteiro
	// Rever a possibilidade de converter BYTES para INTEIRO
	aByteToInt, _ := strconv.Atoi(string(bodyBytes))
	// fmt.Println(aByteToInt)

	return aByteToInt
}

func get_board() [][]int {
	var jsonstring string
	var listoflists [][]int

	resp, _ := http.Get("http://localhost:8080/tabuleiro")

	// Sinaliza que a última ação a ser feita no programa é o fechamento da resposta
	defer resp.Body.Close()

	// Por fim escreve o conteúdo do feed de rss
	bodyBytes, _ := ioutil.ReadAll(resp.Body)
	jsonstring = string(bodyBytes)

	dec := json.NewDecoder(strings.NewReader(jsonstring))
	dec.Decode(&listoflists)

	return listoflists
}

func send_movement(movement []int) []int {

	var jsonstring string
	var listoflists []int

	resp, _ := http.Get("http://localhost:8080/move?player=" + strconv.Itoa(jogador) + "&coluna=" + strconv.Itoa(movement[0]) + "&linha=" + strconv.Itoa(movement[1]))

	// Sinaliza que a última ação a ser feita no programa é o fechamento da resposta
	defer resp.Body.Close()

	// Por fim escreve o conteúdo do feed de rss
	bodyBytes, _ := ioutil.ReadAll(resp.Body)
	jsonstring = string(bodyBytes)

	// fmt.Println(jsonstring)

	dec := json.NewDecoder(strings.NewReader(jsonstring))
	dec.Decode(&listoflists)

	return listoflists
}

func sub_board(listoflists [][]int) [][]int {

	for x, list := range listoflists {
		// fmt.Println(list)
		for y, value := range list {
			// fmt.Println(value)
			if value == 0 {
				// fmt.Println("ZERO")
				listoflists[x][y] = 1
			}
		}
	}
	return listoflists

}

func copy_board(listoflists [][]int) [][]int {

	var board [][]int = make([][]int, len(listoflists))

	for x, list := range listoflists {
		board[x] = make([]int, len(list))
		for y, value := range list {
			board[x][y] = value
			// fmt.Println(x, y, value)
		}
	}
	return board
}

func get_movements() [][]int {
	var jsonstring string
	var listoflists [][]int

	resp, _ := http.Get("http://localhost:8080/movimentos")

	// Sinaliza que a última ação a ser feita no programa é o fechamento da resposta
	defer resp.Body.Close()

	// Por fim escreve o conteúdo do feed de rss
	bodyBytes, _ := ioutil.ReadAll(resp.Body)
	jsonstring = string(bodyBytes)

	jsonstring = strings.Replace(jsonstring, "(", "[", -1)
	jsonstring = strings.Replace(jsonstring, ")", "]", -1)

	dec := json.NewDecoder(strings.NewReader(jsonstring))
	dec.Decode(&listoflists)

	return listoflists
}

func heuristic(board [][]int, position []int) int {
	// var counter int{0}
	counter := 0
	l := vizinhos(board, position)
	// fmt.Println(position, l)

	for _, index := range l {
		// fmt.Println(index)
		//for index := 0; index < len(l); index++ {
		if board[index[0]][index[1]] == 0 {
			counter = counter + 10
		}
		if board[index[0]][index[1]] == jogador { // VERIFICAR o 1
			counter = counter + 20
		}
		if board[index[0]][index[1]] == adversario { // Jogador adversário
			counter = counter - 10
		}

		//}
	}
	return counter
}

func vizinhos(board [][]int, pos []int) [][]int {
	column := pos[0]
	line := pos[1]

	var position []int
	var l [][]int

	if line < len(board[column])-1 { // DOWN
		position = []int{column, line + 1}
		l = append(l, position)
	}

	if column <= len(board)-1 && column != 0 { // DIAGONAL L/D
		// fmt.Println("L/D")
		if line != len(board[column])-1 && column < 6 {
			position = []int{column - 1, line}
			l = append(l, position)
		} else if column >= 6 {
			position = []int{column - 1, line + 1}
			l = append(l, position)
		}
	}

	if column <= len(board)-1 && column != 0 { // DIAGONAL L/U
		// fmt.Println("L/U")
		if column < 6 && line != 0 {
			position = []int{column - 1, line - 1}
			l = append(l, position)
		} else if column >= 6 {
			position = []int{column - 1, line}
			l = append(l, position)
		}
	}

	if line != 0 {
		position = []int{column, line - 1} // UP
		l = append(l, position)
	}

	if column < len(board)-1 { // DIAGONAL R/U
		// fmt.Println("DIAGONAL D/U")
		if column < 5 {
			position = []int{column + 1, line}
			l = append(l, position)
		} else if column >= 5 && line != 0 {
			position = []int{column + 1, line - 1}
			l = append(l, position)
		}
	}

	if column < len(board)-1 { // DIAGONAL R/D
		// fmt.Println("DIAGONAL R/D")
		if column < 5 {
			position = []int{column + 1, line + 1}
			l = append(l, position)
		} else if column >= 5 && line != len(board[column+1]) {
			position = []int{column + 1, line}
			l = append(l, position)
		}
	}
	return l
}

// func sorting_plays(plays [][]int) [][]int {

// }

func leaf_generating_matrix(board [][]int, level int, position_father []int) []Node {
	// var x, y, counter, x_size_table, y_size_table //int
	// var position []int
	x_size_table, y_size_table := 0, 0

	list_leaf := []Node{}
	var aux_board [][]int
	x_size_table = len(board)

	for x := 0; x < x_size_table; x++ {
		y_size_table = len(board[x])

		for y := 0; y < y_size_table; y++ {
			if board[x][y] == 0 {
				aux_board = copy_board(board)
				actual_position := []int{x, y}

				if level%2 == 0 {
					aux_board[x][y] = jogador
				} else {
					aux_board[x][y] = adversario
				}

				// if position_father[0] != -1 {
				// 	position = position_father
				// 	// fmt.Println("Position: ", position)
				// 	// fmt.Println("++++++++++++")
				// } else {
				// 	position = actual_position
				// 	// fmt.Println("Position: ", position)
				// }

				// fmt.Println(position)
				// position := []int{x, y}
				// leaf.set_data(position, aux_board)

				//============== HEURISTICA ============
				value_heuristic := heuristic(aux_board, actual_position) // Valor da heuristica
				// fmt.Println("Heuristic: ", value_heuristic)
				//======================================
				// position_father := Node.get_data()

				leaf := Node{actual_position, aux_board, value_heuristic}
				// leaf := Node{position, aux_board, value_heuristic}	// Esse aqio
				list_leaf = append(list_leaf, leaf)
				//======================================
				// fmt.Println(actual_position)
				// fmt.Println(value_heuristic)

				//is_final_state(aux_board)
			}
		}
	}

	return list_leaf
}

func leafs_generating_matrix(father []Node, depth int) {
	//var size_list_father, level int
	//var board [][]int
	//level := 0

	//========================================================================
	board := father[0]
	copy(father, father[1:])
	father = father[:len(father)-1]

	position := []int{-1, -1}
	father = append(father, leaf_generating_matrix(board.get_board(), 0, position)...)
	//========================================================================

	for level := 1; level < depth; level++ {
		size_list_father := len(father)

		for x := 0; x < size_list_father; x++ {

			board := father[0]
			copy(father, father[1:])
			father = father[:len(father)-1]

			//aux := leaf_generating_matrix(board.get_board(), level)

			father = append(father, leaf_generating_matrix(board.get_board(), level, board.get_data())...)
			// father = father[:len(father)-1]
		}
	}
	// fmt.Println(father[1].get_board())
	// fmt.Println(father[79].get_data())
	//========= Realizar Jogada ==========
	sort.Sort(ByHeuristic(father))

	// s := sort.IntsAreSorted(father)

	// sort.SliceStable(father, func(i, j int) bool { return father[i].heuristic < father[j].heuristic })
	// sort.Slice(father[:], func(i, j int) bool { return father[i].heuristic < father[j].heuristic })
	//====================================
	// fmt.Println(father[0].get_heuristic())
	fmt.Println(father[0].get_data())
	fmt.Println(father[0].get_heuristic())
	// valid := true
	// for {
	aux := father[0].get_data()
	aux[0] = aux[0] + 1
	aux[1] = aux[1] + 1

	send_movement(aux)

	fmt.Println(father[0].get_data())
	fmt.Println(father[0].get_heuristic())
	// }
	// send_movement(father[0].get_data())

}

func player() {
	var board, movements [][]int

	for {

		if jogador == get_player() {
			movements = get_movements()
			if len(movements) > 2 {
				position := []int{0, 0}

				board = get_board()
				father := Node{position, board, 0}

				leafs_generating_matrix([]Node{father}, 2)

			} else {
				fmt.Println("...")
			}
			time.Sleep(2 * time.Second)
		}
	}
}

func main() {

	// var aux_board [][]int

	// board := board()
	// fmt.Println("Tabela Original:\n ", board)

	// aux_board := copy_board(board)
	// sub_board := sub_board(board)

	// fmt.Println("Tabela Copiada:\n ", aux_board)
	// fmt.Println("Tabela Modificada:\n ", sub_board)
	start := time.Now()
	player()
	elapsed := time.Since(start)
	log.Printf("Time %s", elapsed)
}
