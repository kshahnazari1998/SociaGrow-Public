import 'package:sociagrowapp/models/user.dart';
import 'package:sociagrowapp/Authenticate/SignIn.dart';
import 'package:sociagrowapp/HomePages/Home.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:sociagrowapp/Authenticate/authenticate.dart';


class Wrapper extends StatefulWidget{
  @override
  createState() => _Wrapper();
}

class _Wrapper extends State<Wrapper> {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  

  @override
  Widget build(BuildContext context) {

    
    final user = Provider.of<User>(context);
    
    
    // return either the Home or Authenticate widget
    if (user == null){
      print('Should Changed 3');
      return Scaffold(
       body: Authenticate()
      );
    }
    else {
      
      return PageData();
      
    }
    
  
  
  }
}