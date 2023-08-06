# django-drf-client
Dynamic client based on coreapi and drf inspired by dotmap and java script


Example

    def get_client(url,username,password):
        from drf_client.client import DrfClient
        return DrfClient(url, username, password)
      
    drfc = get_client('http://server-dns-name','username','password')
    doc(drfc) # it will list possible options based on server
    
    # Example
    drfc.api.<app-name>.<model>.create(**params)
    drfc.api.<app-name>.<model>.list(**params).all()
    drfc.api.<app-name>.<model>.list(**params).first()
    