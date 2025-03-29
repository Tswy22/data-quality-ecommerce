import pandas as pd
from faker import Faker
import random
import uuid
from datetime import timedelta

fake = Faker()

def generate_transaction(transaction_id, has_issue=False, specific_date=None):
    user_id = str(uuid.uuid4())
    product_id = str(uuid.uuid4())
    category = random.choice(['electronics', 'fashion', 'books', 'home', 'toys'])
    amount = round(random.uniform(5.0, 500.0), 2)
    payment_method = random.choice(['credit_card', 'paypal', 'bank_transfer'])
    status = random.choice(['paid', 'void', 'cancel'])
    
    if specific_date:
        timestamp = fake.date_time_between(start_date=specific_date, end_date=specific_date)
    else:
        timestamp = fake.date_time_this_year()

    if has_issue:
        issue_type = random.choices(["missing_initial", "negative_amount"], weights=[0.6, 0.4], k=1)[0]
        if issue_type == "missing_initial":
            status = random.choice(["void", "cancel"])
        elif issue_type == "negative_amount":
            amount = round(random.uniform(-500.0, -5.0), 2)

    return {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "product_id": product_id,
        "category": category,
        "amount": amount,
        "payment_method": payment_method,
        "status": status,
        "timestamp": timestamp,
        "date": timestamp.date()  
    }

def generate_transactions(num_records=1_000_000):
    transactions = []
    for _ in range(num_records):
        has_issue = random.random() < 0.1  
        transaction = generate_transaction(str(uuid.uuid4()), has_issue)
        transactions.append(transaction)

    df = pd.DataFrame(transactions)
    df.to_csv("historical_transaction.csv", index=False)
    print("Completed 1,000,000 data generation!")

def simulate_daily_transactions(days=5, daily_records=10_000):
    for day in range(1, days + 1):
        specific_date = fake.date_this_year(before_today=True, after_today=False) 

        transactions = []
        for _ in range(daily_records):
            has_issue = random.random() < 0.1  
            transaction = generate_transaction(str(uuid.uuid4()), has_issue, specific_date=specific_date)

            random_time = timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )

            timestamp_with_time = pd.to_datetime(specific_date) + random_time
            transaction['timestamp'] = timestamp_with_time 

            transactions.append(transaction)

        df = pd.DataFrame(transactions)
        df.to_csv(f"daily_transaction_day{day}.csv", index=False)
        print(f"Transaction data completed on {specific_date}")

if __name__ == "__main__":
    generate_transactions()
    simulate_daily_transactions()