package db

import (
	"context"
	"encoding/json"
	"log"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

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

func FindActiveInvoice() string {
	collection := GetCollection("invoices", "invoices")
	filter := bson.M{"config.is_active": true}
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
