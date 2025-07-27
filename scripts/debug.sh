# example service down webhook
curl -X POST http://localhost:8180/api/v1/webhooks/service-issue \
     -H "Content-Type: application/json" \
     -d '{"type": "service_down", "message": "The gallery-api is unreachable."}'
