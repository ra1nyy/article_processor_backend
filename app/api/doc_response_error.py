def doc_response_errors(*errors) -> dict:
    doc = {}
    for error in errors:
        doc[error.status_code] = {
            "description": error.detail,
        }

    return doc
