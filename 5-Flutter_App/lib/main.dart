import 'package:flutter/material.dart';
import 'models/user.dart';
import 'services/auth.dart';
import 'package:provider/provider.dart';
import 'wrapper.dart';
import 'package:sociagrowapp/VersionControl.dart';


void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.

 

  @override
  Widget build(BuildContext context) {
    

 
    
    

    return StreamProvider<User>.value(
      value: AuthService().user,
      child: MaterialApp(
        //home: Wrapper(),
        home: Versioncontrol(),
      ),
    );





  }
}

