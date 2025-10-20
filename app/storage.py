import uuid

# In-memory storage
ACCOUNTS = {}       # account_id -> {"balance": int, "currency": str, "label": str}
PAYMENTS = {}       # idempotency_key -> PaymentResponse
PAYMENTS_BY_ID = {} # payment_id -> {"status": str, "resp": dict, "account_id": str}

def generate_payment_id():
    return str(uuid.uuid4())
