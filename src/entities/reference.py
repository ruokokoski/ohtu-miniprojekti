class Reference:
    def __init__(self,
                 reference_id
                 #reference_type,
                 #citation_key,
                 #author,
                 #title,
                 #publisher,
                 #address,
                 #year,
                 ):

        self.id = reference_id
        #self.reference_type = reference_type
        #self.citation_key = citation_key
        #self.author = author
        #self.title = title
        #self.publisher = publisher
        #self.address = address
        #self.year = year

    def __str__(self):
        return f"{self.id}"
