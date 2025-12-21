#!/bin/bash

if [ $# -lt 1 ]; then
  echo "Run with parameter <IP>"
  exit 1
fi

IP="$1"
DAYS="${2:-365}"
ROOT_DAYS="${3:-3650}"
ROOT_CN="${4:-serverCA}"

# ========================
# Step 1: Create CA
# ========================
openssl genrsa -out rootCA.key 4096
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days $ROOT_DAYS -out rootCA.crt -subj "/CN=${ROOT_CN}"

# ========================
# Step 2: Generate server key and CSR
# ========================
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj "/CN=${IP}"

# ========================
# Step 3: Create SAN file
# ========================
cat > san.cnf <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
IP.1 = ${IP}
EOF

# ========================
# Step 4: Sign server certificate
# ========================
openssl x509 -req -in server.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial \
  -out server.crt -days $DAYS -sha256 -extfile san.cnf
