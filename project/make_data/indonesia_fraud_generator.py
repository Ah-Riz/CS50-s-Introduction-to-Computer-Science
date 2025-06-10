import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize with Indonesian locale
fake = Faker('id_ID')

# Create data directory if not exists
os.makedirs('data', exist_ok=True)

# Indonesia bounding box (entire archipelago)
IDN_BOUNDS = {
    'min_lat': -11.0, 'max_lat': 6.0,
    'min_lon': 94.0, 'max_lon': 141.0
}

# Indonesian bank branches (multiple per city)
BANK_BRANCHES = {
    'BRI_JKT_001': [-6.175392, 106.827153],    # Jakarta HQ
    'BRI_JKT_045': [-6.226521, 106.803368],    # Jakarta South
    'BRI_BDG_012': [-6.914744, 107.609810],    # Bandung Central
    'BRI_BDG_078': [-6.952841, 107.584931],    # Bandung North
    'BRI_SBY_023': [-7.257472, 112.752090],    # Surabaya Central
    'BRI_SBY_101': [-7.289054, 112.797327],    # Surabaya East
    'BRI_DPS_007': [-8.670458, 115.212629],    # Denpasar
    'BRI_MKS_003': [-5.147665, 119.432731],    # Makassar
    'BRI_MDN_019': [3.595196, 98.672226],      # Medan
    'BCA_JKT_112': [-6.193125, 106.821810],    # BCA Grand Indonesia
    'BCA_BDG_087': [-6.917464, 107.619125]     # BCA Bandung
}

# Merchant Category Codes (MCC) for Indonesian businesses
MCC_CODES = {
    'Retail': [5411, 5311, 5331, 5611, 5651],
    'F&B': [5812, 5814, 5462, 5499],
    'Electronics': [5732, 5722, 5946],
    'Fashion': [5655, 5621, 5611],
    'Services': [7216, 7230, 7299, 7399]
}
def generate_realistic_location():
    """Generate random GPS within Indonesia"""
    return [
        random.uniform(IDN_BOUNDS['min_lat'], IDN_BOUNDS['max_lat']),
        random.uniform(IDN_BOUNDS['min_lon'], IDN_BOUNDS['max_lon'])
    ]

def generate_realistic_transactions(num_records=10000):
    """Generate raw transaction data without feature engineering"""
    # Create customer base
    customers = {}
    for i in range(5000):
        cust_id = f'C{str(i).zfill(8)}'
        customers[cust_id] = {
            'account_number': fake.bban(),
            'avg_amount': max(50000, int(np.random.normal(300000, 150000)))
        }
    
    # Create merchants
    merchants = []
    for i in range(1000):
        location = generate_realistic_location()
        category = random.choice(list(MCC_CODES.keys()))
        merchants.append({
            'merchant_id': f'M{str(i).zfill(7)}',
            'merchant_name': fake.company(),
            'merchant_category': category,
            'mcc': random.choice(MCC_CODES[category]),
            'location': location
        })
    
    # Generate transactions
    transactions = []
    current_time = datetime.now() - timedelta(days=30)
    
    for _ in range(num_records):
        cust_id = random.choice(list(customers.keys()))
        customer = customers[cust_id]
        merchant = random.choice(merchants)
        
        # Create raw transaction
        tx = {
            'transaction_id': fake.uuid4(),
            'timestamp': current_time,
            'customer_id': cust_id,
            'account_number': customer['account_number'],
            'merchant_id': merchant['merchant_id'],
            'merchant_name': merchant['merchant_name'],
            'merchant_category': merchant['merchant_category'],
            'mcc': merchant['mcc'],
            'amount_idr': max(10000, int(np.random.normal(customer['avg_amount'], customer['avg_amount']*0.3))),
            'currency': 'IDR',
            'customer_lat': random.uniform(IDN_BOUNDS['min_lat'], IDN_BOUNDS['max_lat']),
            'customer_lon': random.uniform(IDN_BOUNDS['min_lon'], IDN_BOUNDS['max_lon']),
            'merchant_lat': merchant['location'][0],
            'merchant_lon': merchant['location'][1],
            'device_id': fake.sha256()[:32],
            'bank_branch': random.choice(list(BANK_BRANCHES.keys())),
            'fraud_probability': 0.0,
            'fraud_type': None,
            'fraud_pattern': None
        }
        
        # Fraud injection logic
        fraud_chance = random.random()
        
        # Credit card fraud (2%)
        if fraud_chance < 0.02:
            tx = inject_credit_card_fraud(tx)
            
        # Card testing (3%)
        elif fraud_chance < 0.05:
            tx = inject_card_testing(tx)
            
        # Money laundering (1.5%)
        elif fraud_chance < 0.065:
            tx = inject_money_laundering(tx)
        
        transactions.append(tx)
        current_time += timedelta(minutes=random.randint(1, 120))
    
    return pd.DataFrame(transactions)

def inject_credit_card_fraud(tx):
    """Inject stolen card patterns"""
    tx['fraud_type'] = 'CreditCardFraud'
    tx['fraud_pattern'] = random.choice(['HighValue', 'OffHours', 'NewDevice'])
    tx['fraud_probability'] = random.uniform(0.85, 0.98)
    
    if tx['fraud_pattern'] == 'HighValue':
        tx['amount_idr'] = random.randint(5000000, 20000000)
    elif tx['fraud_pattern'] == 'OffHours':
        tx['timestamp'] = tx['timestamp'].replace(hour=random.randint(1,4))
    elif tx['fraud_pattern'] == 'NewDevice':
        tx['device_id'] = fake.sha256()[:32]
    
    return tx

def inject_card_testing(tx):
    """Inject card testing patterns"""
    tx['fraud_type'] = 'CardTesting'
    tx['fraud_pattern'] = 'MicroTransactions'
    tx['fraud_probability'] = random.uniform(0.75, 0.90)
    tx['amount_idr'] = random.randint(10000, 50000)
    return tx

def inject_money_laundering(tx):
    """Inject money laundering patterns"""
    tx['fraud_type'] = 'MoneyLaundering'
    tx['fraud_pattern'] = random.choice(['Smurfing', 'TradeBased'])
    tx['fraud_probability'] = random.uniform(0.80, 0.95)
    
    if tx['fraud_pattern'] == 'Smurfing':
        tx['amount_idr'] = random.randint(900000, 999000)  # Below reporting threshold
    elif tx['fraud_pattern'] == 'TradeBased':
        tx['mcc'] = 4829  # Wire transfers
        tx['amount_idr'] = random.randint(5000000, 20000000)
    
    return tx

# Generate dataset
if __name__ == "__main__":
    df = generate_realistic_transactions(100000)
    df.to_csv('data/indonesia_transactions_raw.csv', index=False)