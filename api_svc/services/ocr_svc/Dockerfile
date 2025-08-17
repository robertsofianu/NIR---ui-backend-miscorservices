# Build Go binary
FROM golang:1.24.3-alpine AS builder

WORKDIR /app

# Copy go.mod and go.sum from the root if needed
COPY ../../go.mod ../../go.sum ./
RUN go mod download

# Copy the OCR service code
COPY . .

# Build the Go app
RUN go build -o ocr_svc ./services/ocr_svc/ocr_svc.go

# Final image: includes Python and Go binary
FROM python:3.12-alpine

WORKDIR /app

# Install build dependencies for Python packages (if needed)
RUN apk add --no-cache gcc musl-dev

# Copy Python code and requirements
COPY services/ocr_svc/ocr_svc.py .
COPY services/ocr_svc/requirements.txt .


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Go binary from builder
COPY --from=builder /app/ocr_svc .

# Expose the port your Go app runs on
EXPOSE 8081

# Run the Go service
CMD ["./ocr_svc"]