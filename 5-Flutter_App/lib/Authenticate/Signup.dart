import 'package:flutter/material.dart';
import 'package:sociagrowapp/services/firestore.dart';
import 'package:sociagrowapp/services/auth.dart';
import 'package:email_validator/email_validator.dart';

class SignUp extends StatefulWidget{
  final Function toggleView;
  SignUp({ this.toggleView });

  @override
  createState() => _SignUp();
}

class _SignUp extends State<SignUp> {

  final AuthService _auth = AuthService();
  String error = '';

  // text field state
  String email = '';
  String password = '';
  
  @override
  Widget build(BuildContext context) {
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
                Container(
                  color: Color(0xfff5f5f5),
                  
                  child: TextFormField(
                    onChanged: (val) {
                    setState(() => password = val);
                    },
                    obscureText: true,
                    style: TextStyle(
                      color: Colors.black,
                      fontFamily: 'SFUIDisplay'
                    ),
                    decoration: InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Password',
                      prefixIcon: Icon(Icons.lock_outline),
                      labelStyle: TextStyle(
                          fontSize: 15
                        )
                    ),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.only(top: 20),
                  child: MaterialButton(
                    onPressed: () async {
                        String texterr = '';
                        if (this.password.length < 6)
                          texterr = 'Password has to be more than 7 characters';
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
                          dynamic result = await this._auth.registerWithEmailAndPassword(this.email.trim(), this.password);
                          if (result!=null)
                          {
                            var fc = Firestorecommands();
                            fc.addnewuser(result.uid);
                            //add user to firebase

                          }
                          print(result);
                          setState(() {
                        
                          });
                        if(result == null) {
                          setState(() {
                        error = 'Please supply a valid email';
                        });
                        
                        }
                        

                        }

                    },//since this is only a UI app
                    child: Text('SIGN UP',
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
                              widget.toggleView();
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
  }
}