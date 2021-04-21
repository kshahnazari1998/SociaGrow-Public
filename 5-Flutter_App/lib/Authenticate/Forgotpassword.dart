import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:email_validator/email_validator.dart';
import 'package:sociagrowapp/wrapper.dart';

class Forgotpass extends StatefulWidget{
  
  @override
  createState() => _Forgotpass();
}

class _Forgotpass extends State<Forgotpass> {

  
  String error = '';

  // text field state
  String email = '';
  
  
  @override
  
    Widget build(BuildContext context) {
    
    return Scaffold(
    
    body: Builder(
      // Create an inner BuildContext so that the onPressed methods
      // can refer to the Scaffold with Scaffold.of().
      builder: (BuildContext context) {
    return Stack(
      children: <Widget>[
        Container(
          decoration: BoxDecoration(
            image: DecorationImage(
              image: AssetImage('assets/image2.png'),
              fit: BoxFit.fitWidth,
              alignment: Alignment.topCenter
            )
          ),
        ),
        Container(
          width: MediaQuery.of(context).size.width,
          margin: EdgeInsets.only(top: 270),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            color: Colors.white,
          ),
          child: Padding(
            padding: EdgeInsets.all(23),
            child: ListView(
              children: <Widget>[
                Padding(
                  padding: EdgeInsets.fromLTRB(0, 50, 0, 20),
                  child: Container(
                    color: Color(0xfff5f5f5),
                    child: TextFormField(
                      style: TextStyle(
                        color: Colors.black,
                        fontFamily: 'SFUIDisplay'
                      ),
                      onChanged: (val) {
                      setState(() => email = val);
                      },
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: 'E-mail',
                        prefixIcon: Icon(Icons.person_outline),
                        labelStyle: TextStyle(
                          fontSize: 15
                        )
                      ),
                    ),
                  ),
                ),
                
                Padding(
                  padding: EdgeInsets.only(top: 0),
                  child: MaterialButton(
                    onPressed: () async {
                        String texterr = '';
                        
                        final bool isValid = EmailValidator.validate(this.email.trim());
                        if (isValid==false)
                          texterr = 'Invalid Email.';
                        final snackBar = SnackBar(
                        content: Text(texterr),
                        );
                        if (texterr!='')
                          Scaffold.of(context).showSnackBar(snackBar);
                        else
                        {
                          try
                          {
                            final FirebaseAuth _auth = FirebaseAuth.instance;
                            await _auth.sendPasswordResetEmail(email: this.email.trim());
                            final snackBar = SnackBar(
                            content: Text('Password reset link sent to your email.'),
                            );
                            Scaffold.of(context).showSnackBar(snackBar);
                            await new Future.delayed(const Duration(seconds: 5), () {
                              Navigator.push(
                              context,
                              MaterialPageRoute(builder: (context) => Wrapper()),
                              );
                            });
                            

                            setState(() {
                            });
                          }
                          catch (e)
                          {
                            final snackBar = SnackBar(
                            content: Text('An error occurred'),
                            );
                            Scaffold.of(context).showSnackBar(snackBar);
                          }
                          }
                        
                        
                        

                        },

                    //since this is only a UI app
                    child: Text('Send Reset Password Link to email',
                    style: TextStyle(
                      fontSize: 15,
                      fontFamily: 'SFUIDisplay',
                      fontWeight: FontWeight.bold,
                    ),
                    ),
                    color: Color(0xffff2d55),
                    elevation: 0,
                    minWidth: 400,
                    height: 50,
                    textColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10)
                    ),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.only(top: 5),
                  child: Center(
                    child: Row(
                        mainAxisAlignment: MainAxisAlignment.center ,
                        children: [
                          
                          FlatButton(
                            onPressed: ()
                            {
                                Navigator.push(
                                context,
                                MaterialPageRoute(builder: (context) => Wrapper()),
                              );
                            },
                           child : Text(
                              "Return to Sign In Page",
                              style: TextStyle(
                                fontFamily: 'SFUIDisplay',
                                color: Color(0xffff2d55),
                                fontSize: 15,
                              )
                            
                            )
                          ),
                        ]
                      
                    ),
                  ),
                )
                
              ],
            ),
          ),
        )
      ],
    );
    } )
    );
}
}