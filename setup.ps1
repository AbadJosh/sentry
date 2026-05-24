# Sentry stack setup

# Start any missing containers
Write-Host 'Starting stack...'
docker compose up -d
Write-Host '[OK] Compose done.'

# Wait for Kafka
Write-Host 'Waiting for Kafka to be healthy...'
$kafkaReady = $false
while (-not $kafkaReady) {
    docker exec sentry-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $kafkaReady = $true } else { Start-Sleep -Seconds 3 }
}
Write-Host '[OK] Kafka ready.'

# Topics
$topics = docker exec sentry-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

if ($topics -notcontains 'btcusdt-trades') {
    Write-Host '[ ] btcusdt-trades missing - creating...'
    docker exec sentry-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic btcusdt-trades --partitions 3 --replication-factor 1 | Out-Null
    Write-Host '[OK] btcusdt-trades created.'
} else {
    Write-Host '[OK] btcusdt-trades exists.'
}

if ($topics -notcontains 'btcusdt-trades-dlq') {
    Write-Host '[ ] btcusdt-trades-dlq missing - creating...'
    docker exec sentry-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic btcusdt-trades-dlq --partitions 1 --replication-factor 1 | Out-Null
    Write-Host '[OK] btcusdt-trades-dlq created.'
} else {
    Write-Host '[OK] btcusdt-trades-dlq exists.'
}

if ($topics -notcontains 'btcusdt-trades-connect-dlq') {
    Write-Host '[ ] btcusdt-trades-connect-dlq missing - creating...'
    docker exec sentry-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic btcusdt-trades-connect-dlq --partitions 1 --replication-factor 1 | Out-Null
    Write-Host '[OK] btcusdt-trades-connect-dlq created.'
} else {
    Write-Host '[OK] btcusdt-trades-connect-dlq exists.'
}

# Wait for Kafka Connect
Write-Host 'Waiting for Kafka Connect to be ready...'
$connectReady = $false
while (-not $connectReady) {
    try {
        Invoke-WebRequest -Uri http://localhost:8083/connectors -Method GET -ErrorAction Stop | Out-Null
        $connectReady = $true
    } catch {
        Start-Sleep -Seconds 5
    }
}
Write-Host '[OK] Kafka Connect ready.'

# Connector
$existing = Invoke-WebRequest -Uri http://localhost:8083/connectors -Method GET | Select-Object -ExpandProperty Content

if ($existing -match 'trades-sink') {
    $statusResponse = Invoke-WebRequest -Uri http://localhost:8083/connectors/trades-sink/status -Method GET | Select-Object -ExpandProperty Content
    $connectorState = ($statusResponse | ConvertFrom-Json).connector.state
    Write-Host "[OK] Connector trades-sink already registered (state: $connectorState) -- skipping."
} else {
    Write-Host '[ ] Connector trades-sink missing - submitting...'
    Invoke-WebRequest -Uri http://localhost:8083/connectors -Method POST -ContentType 'application/json' -InFile kafka-connect/trades-sink.json | Out-Null
    Write-Host '[OK] Connector submitted.'
}

Write-Host ''
Write-Host 'Stack is ready. Start the producer with:'
Write-Host '  cd producer; python -m src.main'
