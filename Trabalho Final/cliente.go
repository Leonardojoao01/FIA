package main

import (
	"fmt"
	"log"
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

func heuristic(board [][]int, position []int) int {
	// var counter int{0}
	counter := 0
	l := nei(board, position)
	fmt.Println(position, l)

	for _, index := range l {
		fmt.Println(index)
		//for index := 0; index < len(l); index++ {
		if board[index[0]][index[1]] == 0 {
			counter = counter + 10
		}
		if board[index[0]][index[1]] == 1 { // VERIFICAR o 1
			counter = counter + 20
		}
		if board[index[0]][index[1]] == 2 {
			counter = counter - 10
		}

		//}
	}
	return counter
}

func nei(board [][]int, pos []int) [][]int {
	column := pos[0]
	line := pos[1]

	var position []int
	var l [][]int

	if line == 0 && column > 0 && column < len(board)-1 {
		if column < 5 {
			position = []int{column + 1, line + 1}
			l = append(l, position)
			position = []int{column + 1, line}
			l = append(l, position)

			position = []int{column, line + 1}
			l = append(l, position)

			position = []int{column - 1, line}
			l = append(l, position)

		} else if column > 5 {
			position = []int{column - 1, line + 1}
			l = append(l, position)
			position = []int{column - 1, line}
			l = append(l, position)

			position = []int{column, line + 1}
			l = append(l, position)

			position = []int{column + 1, line}
			l = append(l, position)

		} else {
			position = []int{column - 1, line}
			l = append(l, position)
			position = []int{column, line + 1}
			l = append(l, position)
			position = []int{column + 1, line}
			l = append(l, position)
		}
	} else if column == 0 {
		position = []int{column + 1, line}
		l = append(l, position)

		position = []int{column + 1, line + 1}
		l = append(l, position)

		if line < len(board[column])-1 && line > 0 {
			position = []int{column, line + 1}
			l = append(l, position)

			position = []int{column, line - 1}
			l = append(l, position)

		} else if line < len(board[column])-1 {
			position = []int{column, line + 1}
			l = append(l, position)
		} else if line > 0 {
			position = []int{column, line - 1}
			l = append(l, position)
		}

	} else if column == len(board)-1 {
		position = []int{column - 1, line + 1}
		l = append(l, position)

		position = []int{column - 1, line}
		l = append(l, position)

		if line < len(board[column])-1 && line > 0 {
			position = []int{column, line + 1}
			l = append(l, position)

			position = []int{column, line - 1}
			l = append(l, position)
		} else if line < len(board[column])-1 {
			position = []int{column, line + 1}
			l = append(l, position)
		} else if line > 0 {
			position = []int{column, line - 1}
			l = append(l, position)
		}

	} else if line == len(board[column])-1 && column > 0 && column < len(board)-1 {

		if column < 5 {
			position = []int{column + 1, line + 1}
			l = append(l, position)
			position = []int{column, line - 1}
			l = append(l, position)

			position = []int{column + 1, line}
			l = append(l, position)

			// position = []int{column - 1, line - 1}
			// l = append(l, position)

			position = []int{column - 1, line - 1}
			l = append(l, position)
		} else if column > 5 {
			position = []int{column - 1, line + 1}
			l = append(l, position)
			position = []int{column, line - 1}
			l = append(l, position)

			position = []int{column + 1, line - 1}
			l = append(l, position)

			// position = []int{column - 1, line - 1}
			// l = append(l, position)

			position = []int{column - 1, line}
			l = append(l, position)
		} else {
			position = []int{column - 1, line - 1}
			l = append(l, position)
			position = []int{column, line - 1}
			l = append(l, position)
			position = []int{column + 1, line - 1}
			l = append(l, position)
		}
	} else {
		if column < 5 {
			position = []int{column, line - 1}
			l = append(l, position)

			position = []int{column, line + 1}
			l = append(l, position)

			position = []int{column + 1, line + 1}
			l = append(l, position)

			position = []int{column - 1, line - 1}
			l = append(l, position)

			position = []int{column + 1, line}
			l = append(l, position)

			position = []int{column - 1, line}
			l = append(l, position)

		} else if column == 5 {
			position = []int{column, line - 1}
			l = append(l, position)

			position = []int{column, line + 1}
			l = append(l, position)

			position = []int{column + 1, line - 1}
			l = append(l, position)

			position = []int{column - 1, line - 1}
			l = append(l, position)

			position = []int{column + 1, line}
			l = append(l, position)

			position = []int{column - 1, line}
			l = append(l, position)
		} else {
			position = []int{column, line - 1}
			l = append(l, position)

			position = []int{column, line + 1}
			l = append(l, position)

			position = []int{column + 1, line - 1}
			l = append(l, position)

			position = []int{column - 1, line + 1}
			l = append(l, position)

			position = []int{column + 1, line}
			l = append(l, position)

			position = []int{column - 1, line}
			l = append(l, position)
		}
	}
	return l
}

func neighbors(board [][]int, position_t []int) [][]int {
	column := position_t[0]
	line := position_t[1]
	var l [][]int

	if line > 1 {
		position := []int{column, line - 1}
		l = append(l, position) // up
	}

	if (column < 6 || line > 1) && (column < len(board)) {
		fmt.Println("LEN:", len(board))
		if column >= 6 {
			position := []int{column + 1, line - 1}
			l = append(l, position) // upper right
			fmt.Println("A1:   ", position, column)
		} else {
			position := []int{column + 1, line}
			l = append(l, position) // upper right
			fmt.Println("A2:   ", position)
		}
	}

	if (column > 6 || line > 1) && (column > 1) {
		//fmt.Println("U")
		if column > 6 {
			position := []int{column - 1, line}
			l = append(l, position) // upper left
			fmt.Println("U1:   ", position)
		} else {

			position := []int{column - 1, line - 1}
			l = append(l, position) // upper left
			fmt.Println("U2:   ", position)
		}
	}

	if column > 0 {

		if line < len(board[column-1]) {
			position := []int{column, line + 1}
			l = append(l, position) // down
			fmt.Println("1 IF: ", position)
		}
		//fmt.Println("jiuajhsdk")
		if (column < 6 && line < len(board[column])-1) && column < len(board) {
			// fmt.Println("2 IF")
			// fmt.Println("LEN: ", len(board[column])-1)
			// fmt.Println("LINE: ", line)
			if column < 6 {

				position := []int{column + 1, line - 1}
				//fmt.Println("Posição+++++")
				l = append(l, position) // down right
				fmt.Println("21 IF:", position)

				// } else if column > 6 {
				// fmt.Println("Posição")
			} else {
				position := []int{column + 1, line}
				l = append(l, position) // down
				fmt.Println("22 IF:", position)
			}
		}

		if (column > 6 || line < len(board[column])) && column > 1 {
			// fmt.Println("3 IF")
			if column > 6 {

				position := []int{column - 1, line + 1}
				l = append(l, position) // down left
				fmt.Println("31 IF:", position)
			} else {
				// fmt.Println("32 IF")
				position := []int{column - 1, line}
				l = append(l, position) // down left
				fmt.Println("32 IF:", position)
			}
		}
	}

	return l
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
				position := []int{x, y}
				// leaf.set_data(position, aux_board)
				leaf := Node{position, aux_board}

				list_leaf = append(list_leaf, leaf)
				//======================================
				value_heuristic := heuristic(aux_board, position)
				fmt.Println(value_heuristic)

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

			aux := leaf_generating_matrix(board.get_board(), level)

			father = append(father, aux...)
		}
	}
	//fmt.Println(father[0].get_board())
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

		leafs_generating_matrix([]Node{father}, 2)

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
	start := time.Now()
	player()
	elapsed := time.Since(start)
	log.Printf("Time %s", elapsed)
}
