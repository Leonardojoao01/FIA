package main

import (
	// "encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"

	// "encoding/binary"
	"strconv"
	// "strings"
)

func player() int {
	resp, _ := http.Get("http://localhost:8080/jogador")

	// if err != nil {
	// 	s := err.Error()
	// 	fmt.Printf("%q\n", s)
	// }

	// Sinaliza que a última ação a ser feita no programa é o fechamento da resposta
	defer resp.Body.Close()

	// Verifica se o código de status é 200, indicando assim o sucesso da solicitação
	if resp.StatusCode != 200 {
		println(resp.StatusCode)
	}

	// Por fim escreve o conteúdo do feed de rss
	bodyBytes, _ := ioutil.ReadAll(resp.Body)

	// if err2 != nil {
	// 	s := err2.Error()
	// 	fmt.Printf("%q\n", s)
	// }

	// bodyString := binary.BigEndian.Uint64(bodyBytes)

	// fmt.Printf(bodyString)

	aByteToInt, _ := strconv.Atoi(string(bodyBytes))
	fmt.Println(aByteToInt)

	return aByteToInt
}

func main() {

	// Obtém o feed de rss através da url
	resp, err := http.Get("http://localhost:8080/tabuleiro")

	if err != nil {
		s := err.Error()
		fmt.Printf("%q\n", s)
		return
	}

	// Sinaliza que a última ação a ser feita no programa é o fechamento da resposta
	defer resp.Body.Close()

	// Verifica se o código de status é 200, indicando assim o sucesso da solicitação
	if resp.StatusCode != 200 {
		println(resp.StatusCode)
		return
	}

	// Por fim escreve o conteúdo do feed de rss
	bodyBytes, err2 := ioutil.ReadAll(resp.Body)

	if err2 != nil {
		s := err2.Error()
		fmt.Printf("%q\n", s)
		return
	}

	bodyString := string(bodyBytes)
	fmt.Println(bodyString)

	fmt.Println(player())
	// =====================================================
	// var juca int = 2
	// j := 0
	// j = soma(1,1)
	// fmt.Println(j)
	// =====================================================
	// var listoflists [][]int

	// dec := json.NewDecoder(strings.NewReader(bodyString))

	// dec.Decode(&listoflists)

	// var x int = 0

	// for _, list := range listoflists {
	//     // fmt.Println(list)
	//     for _, value := range list{
	// 		fmt.Println(value)
	// 		// x=x+1
	// 		x+=1
	//     }
	// }
	// fmt.Println(x)
}
