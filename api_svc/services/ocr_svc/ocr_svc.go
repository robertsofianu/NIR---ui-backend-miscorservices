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
	var req struct {
		Token string `json:"token"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(400, gin.H{"error": "Invalid JSON payload"})
		return
	}
	invoiceJson := db.FindActiveInvoice(req.Token)
	var invoiceData interface{}
	json.Unmarshal([]byte(invoiceJson), &invoiceData)
	c.JSON(200, gin.H{
		"invoice": invoiceData,
	})
}

func postInvoiceRow(c *gin.Context) {
	from, err := c.MultipartForm()
	if err != nil {
		c.JSON(400, gin.H{"error": "Invalid multipart form"})
		return
	}
	files := from.File["images"]
	if len(files) == 0 {
		c.JSON(400, gin.H{"error": "No images uploaded"})
		return
	}
	token := db.CreateToken(db.DefaultUser)
	saved := []gin.H{}
	for _, file := range files {
		f, err := file.Open()
		if err != nil {
			saved = append(saved, gin.H{"filename": file.Filename, "error": "Failed to open"})
			continue
		}
		data := make([]byte, file.Size)
		_, err = f.Read(data)
		if err != nil {
			saved = append(saved, gin.H{"filename": file.Filename, "error": "Failed to read"})
			continue
		}
		collection := db.GetCollection("images", "images")
		doc := map[string]interface{}{
			"filename":     file.Filename,
			"data":         data,
			"content_type": file.Header.Get("Content-Type"),
			"token":        token,
		}
		_, err = collection.InsertOne(c, doc)
		if err != nil {
			saved = append(saved, gin.H{"filename": file.Filename, "error": "MongoDB error"})
			continue
		}
		saved = append(saved, gin.H{"filename": file.Filename, "status": "saved"})
		defer f.Close()
	}
	cmd := exec.Command("sh", "-c", "python3 services/ocr_svc/ocr_svc.py --token "+token)
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println("Error:", err)
	}
	fmt.Println(string(output))
	c.JSON(200, gin.H{"files": saved, "token": token})
}

func main() {
	r := gin.Default()
	r.Use(cors.Default())

	r.POST("/invoice", getInvoiceDetails)
	r.POST("/multi-image", postInvoiceRow)

	r.Run(":8081")
}
