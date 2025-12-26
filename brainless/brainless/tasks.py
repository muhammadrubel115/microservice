# brainless/tasks.py
@shared_task
def handle_user_event(payload):
    apply_rules(payload)
def apply_rules(user_event):
    # Process user event and apply business rules
    if user_event["action"] == "purchase":
        process_purchase(user_event)
        return {"status": "purchase_processed"}
    elif user_event["action"] == "signup":
        process_signup(user_event)
        return {"status": "signup_processed"}
    return {"status": "no_action"}
def process_purchase(event):
    # Logic to process purchase event
    pass
def process_signup(event):
    # Logic to process signup event
    pass
