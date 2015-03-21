# TAPP_SERVER


## API

    /api/v1/get_user_info
      input = {"username" : ______}
      output: 
      {
          "success": "true",
          "first_name" : _______,
          "last_name" : _______,
          "username" : _______,
          "email" : _______,
          "phone_number" : __________
      }
      
    /api/v1/login
      input = {
        "username": ______,
        "password": _______
      }
      output = 
      {
          "success": "true",
          "sessionid": __________
      }
      
    /api/v1/logout,
      input = {
        "sessionid": ________
      }
      output = {
        "success": "true"
      }
      
    /api/v1/force_logout
      input = {
        "username": ________
      }
      output = {
        "success": "true",
        "message": "Deleted all sessions for user"
      }
      
    /api/v1/is_logged_in
      input = {
        "username": ______
      }
      output = {
        "is_logged_in": True or False
      }
      
    /api/v1/register
      input = {
        "first_name": _______,
        "last_name": _______,
        "username": _________,
        "email":_________,
        "password": _________,
        "phone_num":________,
        "pin":_________
      }
