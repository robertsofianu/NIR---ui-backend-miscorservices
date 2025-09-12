package main

import (
	"io"
	"log"
	"net/http"
	"net/url"
)

func main() {
	http.HandleFunc("/ocr", func(w http.ResponseWriter, r *http.Request) {
		resp, err := http.DefaultClient.Do(&http.Request{
			Method: r.Method,
			URL:    mustParseURL("http://localhost:8081/ocr"),
			Body:   r.Body,
		})
		if err != nil {
			w.WriteHeader(http.StatusBadGateway)
			w.Write([]byte("Service unavailable"))
			return
		}
		defer resp.Body.Close()
		w.WriteHeader(resp.StatusCode)
		io.Copy(w, resp.Body)
	})

	http.HandleFunc("/invoice", func(w http.ResponseWriter, r *http.Request) {
		resp, err := http.DefaultClient.Do(&http.Request{
			Method: r.Method,
			URL:    mustParseURL("http://localhost:8082/invoice"),
			Body:   r.Body,
		})
		if err != nil {
			w.WriteHeader(http.StatusBadGateway)
			w.Write([]byte("Service unavailable"))
			return
		}
		defer resp.Body.Close()
		w.WriteHeader(resp.StatusCode)
		io.Copy(w, resp.Body)
	})

	log.Println("API Gateway running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func mustParseURL(u string) *url.URL {
	parsed, err := url.Parse(u)
	if err != nil {
		panic(err)
	}
	return parsed
}
