from lark_api.base.api import get_startup_record_by_user, update_record

def update_pitching_document(open_id, docs_url):
    startup_record = get_startup_record_by_user(open_id)
    startup_record['fields']['Pitching Document'] = {
        "text": "Base",
        "link": docs_url
    }
    startup_record['fields']['Startup Description']  = 'hahahahahahaha'
    print("startup_record")
    print(startup_record)
    update_record(startup_record['id'], startup_record)
