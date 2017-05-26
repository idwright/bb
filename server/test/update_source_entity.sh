curl -X PUT --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{ \ 
   "refs": [ \ 
   ], \ 
   "values": [ \ 
     { \ 
       "data_name": "id", \ 
       "data_type": "integer", \ 
       "data_value": "1", \ 
       "identity": true, \ 
       "source": "test1" \ 
     }, \ 
     { \ 
       "data_name": "sample_type", \ 
       "data_type": "string", \ 
       "data_value": "DNAB", \ 
       "identity": false, \ 
       "source": "test1" \ 
     } \ 
   ] \ 
 }' 'http://localhost:8080/v1/source/test1/1'
