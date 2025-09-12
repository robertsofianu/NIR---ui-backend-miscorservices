package main

import (
	"encoding/json"
	"fmt"
	"nir/framework/db"
	"os/exec"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func logger(c *gin.Context) {
	c.JSON(200, gin.H{
		"Hello": "world",
	})
}

func getInvoiceDetails(c *gin.Context) {
	file, err := c.FormFile("image")
	if err != nil {
		c.JSON(400, gin.H{"error": "No image uploaded"})
		return
	}

	savePath := "api_svc/services/ocr_svc/images/" + file.Filename
	if err := c.SaveUploadedFile(file, savePath); err != nil {
		c.JSON(500, gin.H{"error": "Failed to save image"})
		return
	}

	cmd := exec.Command("sh", "-c", "python3 services/ocr_svc/ocr_svc.py --image_path '"+savePath+"'")
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

	r.POST("/invoice", getInvoiceDetails)
	r.GET("/logger", logger)

	r.Run(":8081")
}
