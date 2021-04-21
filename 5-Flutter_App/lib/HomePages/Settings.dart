import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:sociagrowapp/services/firestore.dart';
import 'package:sociagrowapp/models/user.dart';
import 'package:provider/provider.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class Settings extends StatefulWidget {
  @override
  createState() => _Settings();
}

class _Settings extends State<Settings> {
  var taskperdaytext = '';
  Widget build(BuildContext context) {
    Future tasksNumber() async {
      final user = Provider.of<User>(context);
      String userid = user.uid;
      Firestorecommands fc = Firestorecommands();
      dynamic results = await fc.tasksnum(userid);
      if (results == Null) {
        return 'Something went Wrong :(';
      } else {
        return results;
      }
    }

    return FutureBuilder(
        future: tasksNumber(),
        builder: (BuildContext context, snapshot) {
          if (snapshot.hasData) {
            return Column(children: <Widget>[
              Container(
                width: MediaQuery.of(context).size.width,
                child: Text(
                  'Number of your daily tasks',
                  style: TextStyle(fontWeight: FontWeight.w400),
                ),
                alignment: Alignment.center,
                padding: EdgeInsetsDirectional.fromSTEB(0, 20, 0, 0),
              ),
              Container(
                width: MediaQuery.of(context).size.width,
                child: Text(
                  'We Recommend about 10% of your followers',
                  style: TextStyle(fontWeight: FontWeight.w900, fontSize: 14),
                ),
                alignment: Alignment.center,
                padding: EdgeInsetsDirectional.fromSTEB(0, 5, 0, 0),
              ),
              Container(
                width: MediaQuery.of(context).size.width,
                child: Text(
                  'But no more than 100 Tasks a day!',
                  style: TextStyle(fontWeight: FontWeight.w900, fontSize: 14),
                ),
                alignment: Alignment.center,
                padding: EdgeInsetsDirectional.fromSTEB(0, 5, 0, 20),
              ),
              Container(
                child: TextField(
                  onChanged: (val) {
                    taskperdaytext = val;
                  },
                  
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'Number of current Daily Tasks = ' +
                        snapshot.data.toString(),
                  ),
                ),
                width: MediaQuery.of(context).size.width * 0.8,
                alignment: Alignment.center,
                padding: EdgeInsetsDirectional.fromSTEB(0, 0, 0, 15),
              ),
              Container(
                child: RaisedButton(
                  child: Text('Change Daily Task'),
                  onPressed: () async {
                    var taskperdaynum = -10;
                    try {
                      taskperdaynum = int.parse(taskperdaytext);
                    } catch (e) {
                      final snackBar = SnackBar(
                          content: Text('Please enter a valid number.'));
                      Scaffold.of(context).showSnackBar(snackBar);
                    }
                    if (taskperdaynum > 0 && taskperdaynum < 150) {
                      final user = Provider.of<User>(context);
                      String userid = user.uid;
                      Firestorecommands fc = Firestorecommands();
                      await fc.changetasksnum(userid, taskperdaynum);

                      final snackBar = SnackBar(
                          content:
                              Text('Task per day changed successfuly'));
                      Scaffold.of(context).showSnackBar(snackBar);
                      setState(() {});
                    } else {
                      final snackBar = SnackBar(
                          content:
                              Text('Task must be positive and under 150.'));
                      Scaffold.of(context).showSnackBar(snackBar);
                    }
                  },
                ),
              )
            ]);
          }
          else {
            return SpinKitThreeBounce(
              color: Colors.blue,
            );
          }
        });
  }
}
