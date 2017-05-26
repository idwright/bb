curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{ \ 
   "entity_id": "string", \ 
   "refs": [ \ 
     { \ 
       "data_name": "string", \ 
       "data_type": "string", \ 
       "data_value": "string", \ 
       "fk_name": "", \ 
       "fk_source": "string", \ 
       "identity": false, \ 
       "source": "string", \ 
       "values": [ \ 
         { \ 
           "data_name": "string", \ 
           "data_type": "string", \ 
           "data_value": "string", \ 
           "identity": false, \ 
           "source": "string" \ 
         } \ 
       ] \ 
     } \ 
   ], \ 
   "values": [ \ 
     { \ 
       "data_name": "string", \ 
       "data_type": "string", \ 
       "data_value": "string", \ 
       "identity": false, \ 
       "source": "string" \ 
     } \ 
   ] \ 
 }' 'http://localhost:8080/v1/source/test1/uploadEntity'
