import 'package:flutter/material.dart';
import 'package:sociagrowapp/models/Tasks.dart';
import 'package:sociagrowapp/services/firestore.dart';
import 'package:provider/provider.dart';
import 'package:sociagrowapp/models/user.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class DailyTasks extends StatefulWidget {
  @override
  createState() => _DailyTasks();
}

class _DailyTasks extends State<DailyTasks> {
  Widget build(BuildContext context) {
    Future taskslist() async {
      final user = Provider.of<User>(context);
      String userid = user.uid;
      Firestorecommands fc = Firestorecommands();
      dynamic results = await fc.getaccounttasks(userid);
      if (results == Null) {
        return [Tasks('Something went wrong', '', 0, '', '')];
      } else {
        return results;
      }
    }

    return FutureBuilder(
        future: taskslist(),
        builder: (BuildContext context, snapshot) {
          if (snapshot.hasData) {
            if (snapshot.data.length == 0) {
              return Container(
                  width: MediaQuery.of(context).size.width,
                  child: Column(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Padding(
                            padding:
                                EdgeInsets.only(top: 15, left: 15, right: 15),
                            child: Text(
                                'Looks Like you finished your daily tasks!',style: TextStyle(fontWeight: FontWeight.bold),)),
                        Padding(
                            padding:
                                EdgeInsets.only(top: 15, left: 15, right: 15),
                            child: Text(
                              "If you Just Signed Up please give us 24 hours to analyze your account and also find accounts which are highly probable to be your target audiance. After 24 hours you will be ready to go!",
                              textAlign: TextAlign.center,
                            )),
                        Padding(
                            padding:
                                EdgeInsets.only(top: 15, left: 15, right: 15),
                            child: Text(
                              "New Tasks Are given every day at 4 AM PST. If you don't receive new tasks after 24 hours or the engagement is dropping significantly in the given tasks consider adding new Target Accounts in The Target Account Tab",
                              textAlign: TextAlign.center,
                            ))
                            
                      ]));
            } else
              return Container(
                  child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: <Widget>[
                  Padding(
                      padding: EdgeInsets.only(top: 15),
                      child: Text(
                        'List of your Daily Tasks: ',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      )),
                  Padding(
                      padding: EdgeInsets.only(top: 15),
                      child: Text(
                        'New Tasks Every 24 hours',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      )),
                  Expanded(
                      child: Padding(
                          padding: EdgeInsets.only(top: 15),
                          child: Card(
                              child: ListView.builder(
                                  itemCount: snapshot.data.length,
                                  itemBuilder:
                                      (BuildContext context, int index) {
                                    // If the status is -1 means that account was not found
                                    // if the Status is -2 means that account was private
                                    var account = snapshot.data[index].account;
                                    var task = snapshot.data[index].task;
                                    switch (task) {
                                      case ('Like3'):
                                        {
                                          task = 'Like a few posts';
                                          break;
                                        }
                                      case ('Follow'):
                                        task = 'Follow the account';
                                        break;
                                      case ('Likecomment'):
                                        task = 'Like and write a good comment';
                                        break;
                                    }
                                    var targetAccount =
                                        snapshot.data[index].targetAccount;
                                    targetAccount =
                                        'Audiance of ' + targetAccount;
                                    var likepercentage =
                                        snapshot.data[index].likepercentage *
                                            100;
                                    var likepercentagetext =
                                        'Has engaged with ' +
                                            likepercentage.toString() +
                                            '% of recent content ';
                                    var docid = snapshot.data[index].docuid;
                                    return GestureDetector(
                                        onTap: () async {
                                          var url = 'https://instagram.com/' +
                                              account;
                                          if (await canLaunch(url)) {
                                            await launch(url);
                                          } else {
                                            throw 'Could not launch $url';
                                          }
                                          print('Clicked');
                                        },
                                        child: Card(
                                            child: Container(
                                          height: 110,
                                          child: Row(
                                              mainAxisAlignment:
                                                  MainAxisAlignment
                                                      .spaceBetween,
                                              children: <Widget>[
                                                Column(
                                                    crossAxisAlignment:
                                                        CrossAxisAlignment
                                                            .start,
                                                    children: [
                                                      Padding(
                                                          padding:
                                                              EdgeInsets.only(
                                                                  left: 5,
                                                                  top: 8),
                                                          child: Text(account)),
                                                      Padding(
                                                          padding:
                                                              EdgeInsets.only(
                                                                  left: 5,
                                                                  top: 8),
                                                          child: Text(task)),
                                                      Padding(
                                                          padding:
                                                              EdgeInsets.only(
                                                                  left: 5,
                                                                  top: 8),
                                                          child: Text(
                                                              targetAccount)),
                                                      Padding(
                                                          padding:
                                                              EdgeInsets.only(
                                                                  left: 5,
                                                                  top: 8),
                                                          child: Text(
                                                              likepercentagetext)),
                                                    ]),
                                                Align(
                                                    alignment:
                                                        Alignment.centerRight,
                                                    child: Padding(
                                                      child: MaterialButton(
                                                        shape: RoundedRectangleBorder(
                                                            borderRadius:
                                                                new BorderRadius
                                                                        .circular(
                                                                    18.0),
                                                            side: BorderSide(
                                                                color: Colors
                                                                    .red)),
                                                        child: Text(
                                                          'Done',
                                                          style: TextStyle(
                                                              color:
                                                                  Colors.white),
                                                        ),
                                                        color: Colors.red,
                                                        onPressed: () async {
                                                          
                                                          
                                                          Firestorecommands fc =
                                                              Firestorecommands();
                                                          dynamic results =
                                                              await fc
                                                                  .completetasks(
                                                                      docid);
                                                          if (results ==
                                                              'success') {
                                                            setState(() {});
                                                          } else {
                                                            final snackBar = SnackBar(
                                                                content: Text(
                                                                    'Something went wrong.'));
                                                            Scaffold.of(context)
                                                                .showSnackBar(
                                                                    snackBar);
                                                          }
                                                        },
                                                      ),
                                                      padding: EdgeInsets.only(
                                                          right: 15),
                                                    ))
                                              ]),
                                        )));
                                  }))))
                ],
              ));
          } else {
            return SpinKitThreeBounce(
              color: Colors.blue,
            );
          }
        });
  }
}
