package main

import (
	"fmt"
	// "encoding/json"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"strings"

	// "encoding/binary"
	"strconv"
	// "strings"
)

type Node struct {
	movement []int
	board    [][]int
}

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

func leaf_generating_matrix(board [][]int, level int) []Node {
	// var x, y, counter, x_size_table, y_size_table //int
	x_size_table, y_size_table := 0, 0

	list_leaf := []Node{}
	var aux_board [][]int
	x_size_table = len(board)

	for x := 0; x < x_size_table; x++ {
		y_size_table = len(board[x])

		for y := 0; y < y_size_table; y++ {
			if board[x][y] == 0 {
				aux_board = copy_board(board)

				if level%2 == 0 {
					aux_board[x][y] = 1
				} else {
					aux_board[x][y] = 2
				}

				position := []int{y, x}
				// leaf.set_data(position, aux_board)
				leaf := Node{position, aux_board}

				list_leaf = append(list_leaf, leaf)

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

	for level := 0; level < depth; level++ {
		size_list_father := len(father)

		for x := 0; x < size_list_father; x++ {
			board := father[0]
			copy(father, father[1:])
			father = father[:len(father)-1]

			father = append(father, leaf_generating_matrix(board.get_board(), level)...)
		}
	}
}

func player() {
	var board, movements [][]int

	// movements()
	movements = get_movements()
	// fmt.Println(len(movements))
	if len(movements) > 2 {
		position := []int{0, 0}

		board = get_board()
		father := Node{position, board}

		leafs_generating_matrix([]Node{father}, 3)

	} else {
		fmt.Println("...")
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

	player()

}
