#!/bin/bash

BASE_URL="http://localhost:5000/api/timeline_post"

ID=$RANDOM
NAME="Test User $ID"
EMAIL="test$ID@example.com"
CONTENT="Curl test post $ID"

echo "Creating post..."

POST=$(curl -s -X POST "$BASE_URL" \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")

echo "Server Response: $POST"

POST_ID=$(echo "$POST" | grep -o '"id":[0-9]*' | cut -d ':' -f 2)

echo "Checking post was added..."

GET=$(curl -s "$BASE_URL")

if echo "$GET" | grep -q "$CONTENT"; then
  echo "SUCCESS: Post was added"
else
  echo "FAIL: Post was not found"
  exit 1
fi

echo "Deleting test post ID: $POST_ID..."

curl -s -X DELETE "$BASE_URL/$POST_ID"

echo "Checking post was deleted..."

GET=$(curl -s "$BASE_URL")

if echo "$GET" | grep -q "$CONTENT"; then
  echo "FAIL: Post was not deleted"
  exit 1
else
  echo "SUCCESS: Post was deleted"
fi