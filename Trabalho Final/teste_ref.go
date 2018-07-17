package main

import "fmt"

// Função simples que adiciona 1 a variável a
func add1(a int) int {
	a = a + 1 // alteramos o valor de a
	return a  // retornamos o novo valor de a
}

func main() {
	x := 3
	var aux [][]int

	fmt.Println("x = ", x) // deve mostrar "x = 3"

	x1 := add1(x) // chama add1(x)

	fmt.Println("x+1 = ", x1) // deve mostrar "x+1 = 4"
	fmt.Println("x = ", x)    // deve mostrar "x = 3"
}
