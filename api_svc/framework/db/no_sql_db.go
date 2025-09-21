package db

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var DefaultUser string = "default_user"

func Client() *mongo.Client {
	uri := os.Getenv("MONGODB_URI")
	if uri == "" {
		log.Fatal("MONGODB_URI environment variable not set")
	}
	clientOptions := options.Client().ApplyURI(uri)
	client, err := mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		log.Fatal(err)
	}
	return client
}

func GetCollection(dbName, collectionName string) *mongo.Collection {
	client := Client()
	collection := client.Database(dbName).Collection(collectionName)
	return collection
}

func FindActiveInvoice(token string) string {
	collection := GetCollection("invoices", "invoices")
	filter := bson.M{"config.token": token}
	cursor, err := collection.Find(context.TODO(), filter)
	if err != nil {
		log.Fatal(err)
	}
	var activeInvoices []bson.M
	if err = cursor.All(context.TODO(), &activeInvoices); err != nil {
		log.Fatal(err)
	}
	jsonData, err := json.MarshalIndent(activeInvoices, "", "  ")
	if err != nil {
		log.Fatal(err)
	}
	return string(jsonData)
}

func FindAllInvoices() string {
	collection := GetCollection("invoices", "invoices")
	cursor, err := collection.Find(context.TODO(), bson.M{})
	if err != nil {
		log.Fatal(err)
	}
	var allInvoices []bson.M
	if err = cursor.All(context.TODO(), &allInvoices); err != nil {
		log.Fatal(err)
	}
	jsonData, err := json.MarshalIndent(allInvoices, "", "  ")
	if err != nil {
		log.Fatal(err)
	}
	return string(jsonData)
}

func CreateToken(userName string) string {
	randomNum := rand.Intn(100000000)
	tokenBody := userName + fmt.Sprint(randomNum)
	hash := sha256.Sum256([]byte(tokenBody))
	return hex.EncodeToString(hash[:])
}
