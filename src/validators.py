def valid_favorite(favorite):
    if not favorite["laureateId"] or favorite["laureateId"] ==  0:
        return False, "LaureateId obrigatório e maior que zero" 
    
    return True, ""
