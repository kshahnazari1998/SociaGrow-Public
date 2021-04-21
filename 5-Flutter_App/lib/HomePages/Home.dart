import 'package:flutter/material.dart';
import 'package:sociagrowapp/services/auth.dart';
import 'package:sociagrowapp/HomePages/TargetFollowers.dart';
import 'package:sociagrowapp/HomePages/Dailytasks.dart';
import 'package:sociagrowapp/HomePages/Settings.dart';




int selectedbotnavi = 0;



List <Widget> pages = [new DailyTasks(),new Targetaccounts(),new Settings()];

class PageData extends StatefulWidget
{
  @override
  createState() => _PageData();
}

class _PageData extends State<PageData>
{
  void _changeselectbotnaviindex(int index)
  {
    selectedbotnavi = index;
    setState(() {
    });
  }

  final AuthService _auth = AuthService();

  @override
  Widget build(BuildContext context)
  { 
    
    return Scaffold(
        appBar: AppBar(title: Container(
          child: Image.asset('assets/Logo.png',width: 100,height: 200,),
          padding: EdgeInsetsDirectional.fromSTEB(0, 10, 0  , 0),
        ),
        actions: <Widget>[
          FlatButton(
            child: Text('Sign out'),
            onPressed:  () async {
              await this._auth.signOut();
            },
          ),
        ],
        ),

        body: pages[selectedbotnavi],
        bottomNavigationBar: BottomNavigationBar(
          type: BottomNavigationBarType.fixed,
          items :[
            BottomNavigationBarItem(icon: Icon(Icons.timelapse),title:Text('Daily Tasks')),
            BottomNavigationBarItem(icon: Icon(Icons.assignment_ind),title:Text('Target Accounts')),
            BottomNavigationBarItem(icon: Icon(Icons.settings),title:Text('Settings')),],
          currentIndex: selectedbotnavi,
          onTap: _changeselectbotnaviindex,
          selectedItemColor: Colors.amber[800],
          unselectedItemColor: Colors.black,
          showUnselectedLabels: true,
        )
    );
  }
}
