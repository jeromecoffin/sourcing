from datetime import datetime, timezone, timedelta
from pymongo import MongoClient, errors
import gettext
import os
import read
import create

def initialize_mongodb():
    try:
        # Get the MongoDB URI from environment variables
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')

        # Establish a connection to MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # Timeout after 5 seconds

        # Check the connection by attempting to fetch server information
        client.admin.command('ping')

        # Return the sourcingmain database object
        return client.sourcingmain

    except errors.ServerSelectionTimeoutError as err:
        log_event("Mongodb Timeout", details=err)
        raise SystemExit("MongoDB connection failed. Exiting.")

    except Exception as e:
        log_event("Mongodb Exception", details=e)
        raise


# Calculates various KPIs from MongoDB collections.
# Output dict (e.g kpis["total_projects"])
def calculate_kpis(user_id):

    total_rfis = read.rfis(user_id)

    total_sent_rfis = 0
    suppliersContacted = []

    for rfi in total_rfis:
        suppliersContacted = rfi["suppliers"]
        total_sent_rfis += len(suppliersContacted)


    return {
        "total_rfis": len(total_rfis),
        "total_sent_rfis": total_sent_rfis
    }

# Logs an event with a specific type and details to the MongoDB 'event_logs' collection.
def log_event(event_type, details=None):
    utc_plus_7 = timezone(timedelta(hours=7))
    event_data = {
        "event_type": event_type,
        "timestamp": datetime.now(utc_plus_7).strftime('%Y%m%d%H%M%S'),
        "details": details
    }
    create.log(event_data)

# Configures gettext for translations based on the user's language preference.
def translate(user_id):

    # 'en' pour anglais, 'vi' pour vietnamien, 'fr' pour français
    language = read.language(user_id)

    # Configurer le chemin des fichiers de traduction
    locales_dir = os.path.join(os.path.dirname(__file__), 'locales')

    gettext.bindtextdomain('messages', locales_dir)
    gettext.textdomain('messages')

    language = gettext.translation('messages', locales_dir, languages=[language])
    language.install()

    return language.gettext