package main

import (
	"encoding/json"
	"fmt"
	"nir/framework/db"
	"os/exec"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func getInvoiceDetails(c *gin.Context) {
	cmd := exec.Command("bash", "-c", "python3 services/ocr_svc/ocr_svc.py --image_path '/Users/sofianurobert/Desktop/Nir Proj/WhatsApp Image 2025-08-12 at 22.19.08.jpeg'")
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println("Error:", err)
	}
	fmt.Println(string(output))
	invoiceJson := db.FindActiveInvoice()
	var invoiceData interface{}
	json.Unmarshal([]byte(invoiceJson), &invoiceData)
	c.JSON(200, gin.H{
		"invoice": invoiceData,
	})
}

func main() {
	r := gin.Default()
	r.Use(cors.Default())

	r.GET("/invoice", getInvoiceDetails)

	r.Run(":8082")
}
