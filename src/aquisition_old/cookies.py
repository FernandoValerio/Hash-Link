from requests import Session

def export_cookies(session:Session)->dict:
    return session.cookies.get_dict()
