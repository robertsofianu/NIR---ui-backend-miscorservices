package main

import (
	"fmt"
	"os/exec"
)

func main() {
	cmd := exec.Command("bash", "-c", "python3 ")
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println("Error:", err)
	}
	fmt.Println(string(output))
}
