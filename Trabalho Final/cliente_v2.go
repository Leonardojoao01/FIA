package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"sort"
	"strconv"
	"strings"
	"time"
)

var jogador int = 1
var adversario int = 2

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
		for y, value := range list {
			if value == 0 {
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

func heuristic(board [][]int, position []int, level int) int {
	// var counter int{0}
	counter := 0
	l := vizinhos(board, position)
	// fmt.Println(position, l)

	for _, index := range l {
		if board[index[0]][index[1]] == 0 {
			counter = counter + 10
		}
		if board[index[0]][index[1]] == jogador { // VERIFICAR o 1
			counter = counter + 20
		}
		if board[index[0]][index[1]] == adversario { // Jogador adversário
			counter = counter - 10
		}
	}
	// her := 0.1

	// //==================JOGADOR =====================
	// value_neighbor_down, count_d := find_neighbor_down(board, position, jogador)
	// value_neighbor_left_down, count_ld := find_neighbor_left_down(board, position, jogador)
	// value_neighbor_left_up, count_lu := find_neighbor_left_up(board, position, jogador)
	// value_neighbor_up, count_u := find_neighbor_up(board, position, jogador)
	// value_neighbor_right_up, count_ru := find_neighbor_right_up(board, position, jogador)
	// value_neighbor_right_down, count_rd := find_neighbor_right_down(board, position, jogador)

	value_neighbor_down, _ := find_neighbor_down(board, position, jogador)
	value_neighbor_left_down, _ := find_neighbor_left_down(board, position, jogador)
	value_neighbor_left_up, _ := find_neighbor_left_up(board, position, jogador)
	value_neighbor_up, _ := find_neighbor_up(board, position, jogador)
	value_neighbor_right_up, _ := find_neighbor_right_up(board, position, jogador)
	value_neighbor_right_down, _ := find_neighbor_right_down(board, position, jogador)

	// counter = counter + value_neighbor_down*count_d*her + value_neighbor_left_down*count_ld*her + value_neighbor_left_up*count_lu*her + value_neighbor_up*count_u*her + value_neighbor_right_up*count_ru*her + value_neighbor_right_down*count_rd*her
	// counter = counter + int(float64(value_neighbor_down*count_d)*her) + int(float64(value_neighbor_left_down*count_ld)*her) + int(float64(value_neighbor_left_up*count_lu)*her) + int(float64(value_neighbor_up*count_u)*her) + int(float64(value_neighbor_right_up*count_ru)*her) + int(float64(value_neighbor_right_down*count_rd)*her)
	// counter = counter + value_neighbor_down + value_neighbor_left_down + value_neighbor_left_up + value_neighbor_up + value_neighbor_right_up + value_neighbor_right_down
	her := 1

	// fmt.Println("level: ", level)

	if level == 0 {
		counter = counter + value_neighbor_down*her*5 + value_neighbor_left_down*her*5 + value_neighbor_left_up*her*5 + value_neighbor_up*her*5 + value_neighbor_right_up*her*5 + value_neighbor_right_down*her*5
		fmt.Println("Entrou: ", counter)
	} else {

		counter = counter + value_neighbor_down + value_neighbor_left_down + value_neighbor_left_up + value_neighbor_up + value_neighbor_right_up + value_neighbor_right_down
		// fmt.Println("Counter: ", counter)
	}

	//==================ADVERSARIO =====================
	value_neighbor_down, _ = find_neighbor_down(board, position, adversario)
	value_neighbor_left_down, _ = find_neighbor_left_down(board, position, adversario)
	value_neighbor_left_up, _ = find_neighbor_left_up(board, position, adversario)
	value_neighbor_up, _ = find_neighbor_up(board, position, adversario)
	value_neighbor_right_up, _ = find_neighbor_right_up(board, position, adversario)
	value_neighbor_right_down, _ = find_neighbor_right_down(board, position, adversario)
	// //=================================================
	// // valeu_final := is_final_state(board)

	// // valeu_final = valeu_final + counter
	// // fmt.Println(valeu_final)
	if level == 0 {
		counter = counter + value_neighbor_down*her*5 + value_neighbor_left_down*her*5 + value_neighbor_left_up*her*5 + value_neighbor_up*her*5 + value_neighbor_right_up*her*5 + value_neighbor_right_down*her*5
		fmt.Println("Entrou: ", counter)
	} else {

		counter = counter + value_neighbor_down + value_neighbor_left_down + value_neighbor_left_up + value_neighbor_up + value_neighbor_right_up + value_neighbor_right_down
		// fmt.Println("Counter: ", counter)
	}

	counter = counter + value_neighbor_down + value_neighbor_left_down + value_neighbor_left_up + value_neighbor_up + value_neighbor_right_up + value_neighbor_right_down
	// her := level
	// counter = counter + value_neighbor_down*her + value_neighbor_left_down*her + value_neighbor_left_up*her + value_neighbor_up*her + value_neighbor_right_up*her + value_neighbor_right_down*her

	return counter
}

// =====================================================================================

func find_neighbor_down(board [][]int, position []int, current_player int) (int, int) {
	var counter int = 0
	var number_neighbor []int

	aux := true
	current_position := position

	var current_player_aux int
	if current_player == 1 {
		current_player_aux = 2
	} else {
		current_player_aux = 1
	}

	for aux {
		number_neighbor = vizinho_down(board, current_position)
		if len(number_neighbor) > 0 {
			if board[number_neighbor[0]][number_neighbor[1]] == current_player_aux {
				counter = counter + 1
			} else {
				aux = false
			}
		} else {
			aux = false
		}
		current_position = number_neighbor
	}
	aux_counter := counter

	if counter > 2 {
		counter = counter * 100
	}
	return counter, aux_counter
}

func vizinho_down(board [][]int, pos []int) []int {
	column := pos[0]
	line := pos[1]

	var position []int
	// var l [][]int

	if line < len(board[column])-1 { // DOWN
		position = []int{column, line + 1}
		// l = append(l, position)
	}
	return position
}

// =======================================================================================

func find_neighbor_left_down(board [][]int, position []int, current_player int) (int, int) {
	var counter int = 0
	var number_neighbor []int

	aux := true
	current_position := position

	var current_player_aux int
	if current_player == 1 {
		current_player_aux = 2
	} else {
		current_player_aux = 1
	}

	for aux {
		number_neighbor = vizinho_left_down(board, current_position)
		if len(number_neighbor) > 0 {
			if board[number_neighbor[0]][number_neighbor[1]] == current_player_aux {
				counter = counter + 1
			} else {
				aux = false
			}
		} else {
			aux = false
		}
		current_position = number_neighbor
	}

	aux_counter := counter

	if counter > 2 {
		counter = counter * 100
	}
	return counter, aux_counter
}

func vizinho_left_down(board [][]int, pos []int) []int {
	column := pos[0]
	line := pos[1]

	var position []int
	// var l [][]int

	if column <= len(board)-1 && column != 0 { // DIAGONAL L/D
		// fmt.Println("L/D")
		if line != len(board[column])-1 && column < 6 {
			position = []int{column - 1, line}
			// l = append(l, position)
		} else if column >= 6 {
			position = []int{column - 1, line + 1}
			// l = append(l, position)
		}
	}
	return position
}

//========================================================================================

func find_neighbor_left_up(board [][]int, position []int, current_player int) (int, int) {
	var counter int = 0
	var number_neighbor []int

	aux := true
	current_position := position

	var current_player_aux int
	if current_player == 1 {
		current_player_aux = 2
	} else {
		current_player_aux = 1
	}

	for aux {
		number_neighbor = vizinho_left_up(board, current_position)
		if len(number_neighbor) > 0 {
			if board[number_neighbor[0]][number_neighbor[1]] == current_player_aux {
				counter = counter + 1
			} else {
				aux = false
			}
		} else {
			aux = false
		}
		current_position = number_neighbor
	}
	aux_counter := counter

	if counter > 2 {
		counter = counter * 100
	}
	return counter, aux_counter
}

func vizinho_left_up(board [][]int, pos []int) []int {
	column := pos[0]
	line := pos[1]

	var position []int
	// var l [][]int

	if column <= len(board)-1 && column != 0 { // DIAGONAL L/U
		// fmt.Println("L/U")
		if column < 6 && line != 0 {
			position = []int{column - 1, line - 1}
			// l = append(l, position)
		} else if column >= 6 {
			position = []int{column - 1, line}
			// l = append(l, position)
		}
	}
	return position
}

//========================================================================================
func find_neighbor_up(board [][]int, position []int, current_player int) (int, int) {
	var counter int = 0
	var number_neighbor []int

	aux := true
	current_position := position

	var current_player_aux int
	if current_player == 1 {
		current_player_aux = 2
	} else {
		current_player_aux = 1
	}

	for aux {
		number_neighbor = vizinho_up(board, current_position)
		if len(number_neighbor) > 0 {
			if board[number_neighbor[0]][number_neighbor[1]] == current_player_aux {
				counter = counter + 1
			} else {
				aux = false
			}
		} else {
			aux = false
		}
		current_position = number_neighbor
	}
	aux_counter := counter

	if counter > 2 {
		counter = counter * 100
	}
	return counter, aux_counter
}

func vizinho_up(board [][]int, pos []int) []int {
	column := pos[0]
	line := pos[1]

	var position []int
	// var l [][]int

	if line != 0 {
		position = []int{column, line - 1} // UP
		// l = append(l, position)
	}
	return position
}

//  ======================================================================================

func find_neighbor_right_up(board [][]int, position []int, current_player int) (int, int) {
	var counter int = 0
	var number_neighbor []int

	aux := true
	current_position := position

	var current_player_aux int
	if current_player == 1 {
		current_player_aux = 2
	} else {
		current_player_aux = 1
	}

	for aux {
		number_neighbor = vizinho_right_up(board, current_position)
		if len(number_neighbor) > 0 {
			if board[number_neighbor[0]][number_neighbor[1]] == current_player_aux {
				counter = counter + 1
			} else {
				aux = false
			}
		} else {
			aux = false
		}
		current_position = number_neighbor
	}
	aux_counter := counter

	if counter > 2 {
		counter = counter * 100
	}
	return counter, aux_counter
}

func vizinho_right_up(board [][]int, pos []int) []int {
	column := pos[0]
	line := pos[1]

	var position []int
	// var l [][]int

	if column < len(board)-1 { // DIAGONAL R/U
		// fmt.Println("DIAGONAL D/U")
		if column < 5 {
			position = []int{column + 1, line}
			// l = append(l, position)
		} else if column >= 5 && line != 0 {
			position = []int{column + 1, line - 1}
			// l = append(l, position)
		}
	}
	return position
}

//  ======================================================================================

func find_neighbor_right_down(board [][]int, position []int, current_player int) (int, int) {
	var counter int = 0
	var number_neighbor []int

	aux := true
	current_position := position

	var current_player_aux int
	if current_player == 1 {
		current_player_aux = 2
	} else {
		current_player_aux = 1
	}

	for aux {
		number_neighbor = vizinho_right_down(board, current_position)
		if len(number_neighbor) > 0 {
			if board[number_neighbor[0]][number_neighbor[1]] == current_player_aux {
				counter = counter + 1
			} else {
				aux = false
			}
		} else {
			aux = false
		}
		current_position = number_neighbor
	}
	aux_counter := counter

	if counter > 2 {
		counter = counter * 100
	}
	return counter, aux_counter
}

func vizinho_right_down(board [][]int, pos []int) []int {
	column := pos[0]
	line := pos[1]

	var position []int
	// var l [][]int

	if column < len(board)-1 { // DIAGONAL R/D
		// fmt.Println("DIAGONAL R/D")
		if column < 5 {
			position = []int{column + 1, line + 1}
			// l = append(l, position)
		} else if column >= 5 && line != len(board[column+1]) {
			position = []int{column + 1, line}
			// l = append(l, position)
		}
	}
	return position
}

// =======================================================================================

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

//==============================================================================

func neighbors(board [][]int, column int, line int) []int {
	var l []int
	// var position []int

	if line > 1 {
		// position = []int{column, line - 1}
		l = append(l, (column))
		l = append(l, (line - 1))
	}

	if (column < 6 || line > 1) && (column < len(board)) {
		if column >= 6 {
			// position = []int{column + 1, line - 1}
			l = append(l, (column + 1))
			l = append(l, (line - 1))

		} else {
			// position = []int{column + 1, line}
			l = append(l, (column + 1))
			l = append(l, (line))
		}
	}

	if (column > 6 || line > 1) && (column > 1) {
		if column > 6 {
			// position = []int{column - 1, line}
			l = append(l, (column - 1))
			l = append(l, (line))
		} else {
			// position = []int{column - 1, line - 1}
			l = append(l, (column - 1))
			l = append(l, (line - 1))
		}
	}

	if line < len(board[column-1]) {
		// position = []int{column, line + 1}
		l = append(l, (column))
		l = append(l, (line + 1))
	}
	// l.append((column, line+1))  # down

	if (column < 6 || line < len(board[column-1])) && column < len(board) {
		if column < 6 {
			// position = []int{column + 1, line + 1}
			l = append(l, (column + 1))
			l = append(l, (line + 1))
			// l.append((column+1, line+1))  // down right
		} else {
			// position = []int{column + 1, line}
			l = append(l, (column + 1))
			l = append(l, (line))
			// l.append((column+1, line))  // down right
		}
	}

	if (column > 6 || line < len(board[column-1])) && column > 1 {
		if column > 6 {
			// position = []int{column - 1, line + 1}
			l = append(l, (column - 1))
			l = append(l, (line + 1))
			// l.append((column-1, line+1))  // down left
		} else {
			// position = []int{column - 1, line}
			l = append(l, (column - 1))
			l = append(l, (line))
			// l.append((column-1, line)) // down left
		}
	}

	return l
}

//=========================================================================================

func leaf_generating_matrix(board [][]int, level int, position_father []int, hey int, level_aux int) []Node {
	// var x, y, counter, x_size_table, y_size_table //int
	var position []int
	x_size_table, y_size_table := 0, 0

	list_leaf := []Node{}
	var aux_board [][]int
	x_size_table = len(board)

	heu_aux := 0

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

				if position_father[0] != -1 {
					position = position_father
					heu_aux = hey
					// fmt.Println("Position: ", position)
					// fmt.Println("++++++++++++")
				} else {
					position = actual_position
					heu_aux = 0
					// fmt.Println("Position: ", position)
				}

				// fmt.Println(position)
				// position := []int{x, y}
				// leaf.set_data(position, aux_board)

				//============== HEURISTICA ============
				value_heuristic := heuristic(aux_board, actual_position, level_aux) // Valor da heuristica
				// fmt.Println("Heuristic: ", value_heuristic)
				//======================================
				// position_father := Node.get_data()

				heu_aux = heu_aux + value_heuristic
				// fmt.Println("HEY: ", heu_aux, value_heuristic)

				leaf := Node{position, aux_board, heu_aux}
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

	//========================================================================
	board := father[0]
	copy(father, father[1:])
	father = father[:len(father)-1]

	position := []int{-1, -1}
	father = append(father, leaf_generating_matrix(board.get_board(), 0, position, 0, 0)...)
	//========================================================================

	for level := 1; level < depth; level++ {
		size_list_father := len(father)

		for x := 0; x < size_list_father; x++ {

			board := father[0]
			copy(father, father[1:])
			father = father[:len(father)-1]
			// if level == 1 {
			// 	fmt.Println("Level: ", level)

			// }

			father = append(father, leaf_generating_matrix(board.get_board(), level, board.get_data(), board.get_heuristic(), level)...)
		}
	}
	// fmt.Println(father[1].get_board())
	// fmt.Println(father[79].get_data())
	//========= Realizar Jogada ==========
	sort.Sort(ByHeuristic(father))
	//====================================
	// fmt.Println(father[0].get_data())
	// fmt.Println(father[0].get_heuristic())
	aux := father[0].get_data()
	aux[0] = aux[0] + 1
	aux[1] = aux[1] + 1
	fmt.Println("Heuristic: ", father[0].get_heuristic())
	fmt.Println("Heuristic: ", father[0].get_data())
	send_movement(aux)

	// fmt.Println(father[0].get_data())
	// fmt.Println(father[0].get_heuristic())

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
			time.Sleep(time.Second * 1)
		}
	}
}

func main() {

	start := time.Now()
	player()
	elapsed := time.Since(start)
	log.Printf("Time %s", elapsed)

}
