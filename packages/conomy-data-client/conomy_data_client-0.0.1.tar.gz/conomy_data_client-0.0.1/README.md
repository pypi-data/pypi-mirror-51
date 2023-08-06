Conmy Data Api Client for Python
===================

Installation:

    pip install conomy_data_client

Usage

    from conomy_data_client import Client

    token = 'lalalalalalala'
    cc = Client(token) 

    issuers = cc.get_issurs()    # return list of issuers
