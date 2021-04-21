import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:sociagrowapp/models/user.dart';
import 'package:sociagrowapp/models/TargetAccounts.dart';
import 'package:sociagrowapp/services/firestore.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class Targetaccounts extends StatefulWidget {
  @override
  createState() => _Targetaccounts();
}

class _Targetaccounts extends State<Targetaccounts> {
  String addaccounttext;

  Widget build(BuildContext context) {
    Future targetaccountslist() async {
      final user = Provider.of<User>(context);
      String userid = user.uid;
      Firestorecommands fc = Firestorecommands();
      dynamic results = await fc.gettargetaccountslist(userid);
      if (results == Null) {
        return [TargetAccount('Something went wrong', 0)];
      } else {
        return results;
      }
    }

    return FutureBuilder(
        future: targetaccountslist(),
        builder: (BuildContext context, snapshot) {
          if (snapshot.hasData) {
            return Container(
                child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                /*
        Padding(
            padding: EdgeInsets.only(top: 15),
            child: Text(
              'Add your Target Accounts here (50 Accounts Limit)',
              style: TextStyle(fontWeight: FontWeight.bold),
            )), */
                Padding(
                  padding: EdgeInsets.only(top: 10),
                  child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        Text(
                          "Don't know what a Target account is? Press here!",
                          style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 12.5,
                              color: Colors.red),
                        ),
                        Padding(
                            padding: EdgeInsets.only(left: 0),
                            child: IconButton(
                              icon: Icon(Icons.info),
                              iconSize: 25,
                              onPressed: () {
                                showDialog(
                                    context: context,
                                    builder: (_) => CupertinoAlertDialog(
                                            title: Text('Target Account'),
                                            content: Text(
                                                'What is a Target Account? Target Accounts are accounts which have the same target audiance as you. For example someone who is posting in the same niche as you and you wish to have as many followers as them. By adding these accounts we will be able to prepare strategies to maximize your growth. Make Sure the Accounts you add are public!'),
                                            actions: [
                                              new FlatButton(
                                                child: const Text("Close"),
                                                onPressed: () =>
                                                    Navigator.pop(context),
                                              ),
                                            ]));
                              },
                            )),
                      ]),
                ),
                Padding(
                  child: Text('Add Target Accounts Here!'),
                  padding: EdgeInsets.only(top: 10, bottom: 15),
                ),
                Container(
                    width: MediaQuery.of(context).size.width * 0.8,
                    child: TextFormField(
                      style: TextStyle(
                          color: Colors.black, fontFamily: 'SFUIDisplay'),
                      onChanged: (val) {
                        addaccounttext = val;
                      },
                      decoration: InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: 'Target Account Username',
                          prefixIcon: Icon(Icons.person_outline),
                          labelStyle: TextStyle(fontSize: 15)),
                    )),
                Padding(
                    padding: EdgeInsets.only(top: 20, bottom: 15),
                    child: MaterialButton(
                      //since this is only a UI app
                      onPressed: () async {
                        if (addaccounttext != '') {
                          final user = Provider.of<User>(context);
                          String userid = user.uid;
                          Firestorecommands fc = Firestorecommands();
                          dynamic results =
                              await fc.addtargetaccount(userid, addaccounttext);
                          if (results == 'success') {
                            final snackBar = SnackBar(
                                content: Text('User Added Successfuly.'));
                            Scaffold.of(context).showSnackBar(snackBar);
                          } else if (results == 'Exists') {
                            final snackBar =
                                SnackBar(content: Text('User Already Exists.'));
                            Scaffold.of(context).showSnackBar(snackBar);
                          } else if (results == 'Toomany') {
                            final snackBar = SnackBar(
                                content: Text('Maximum 50 users allowed.'));
                            Scaffold.of(context).showSnackBar(snackBar);
                          } else {
                            final snackBar = SnackBar(
                                content: Text('Something went Wrong.'));
                            Scaffold.of(context).showSnackBar(snackBar);
                          }
                          setState(() {});
                        }
                      },
                      child: Text(
                        'Add Account',
                        style: TextStyle(
                          fontSize: 15,
                          fontFamily: 'SFUIDisplay',
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      color: Colors.blue,
                      elevation: 0,
                      minWidth: 400,
                      height: 50,
                      textColor: Colors.white,
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10)),
                    )),
                Divider(
                  thickness: 3,
                  color: Colors.blue,
                ),
                Padding(
                    padding: EdgeInsets.only(top: 15),
                    child: Text(
                      'List of your target accounts: (Scroll to see all)',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    )),
                Expanded(
                    child: Padding(
                        padding: EdgeInsets.only(top: 15),
                        child: Card(
                            child: ListView.builder(
                                itemCount: snapshot.data.length,
                                itemBuilder: (BuildContext context, int index) {
                                  // If the status is -1 means that account was not found
                                  // if the Status is -2 means that account was private
                                  var stats = snapshot.data[index].status;
                                  var cardtext = snapshot.data[index].name;
                                  var cardcolor = Colors.white;
                                  switch (stats) {
                                    case 0:
                                      {
                                        cardcolor = Colors.white;
                                        cardtext = snapshot.data[index].name;
                                      }
                                      break;
                                    case -1:
                                      {
                                        cardcolor = Colors.red;
                                        cardtext = snapshot.data[index].name +
                                            "   Account doesen't exist!";
                                      }
                                      break;
                                    case -2:
                                      {
                                        cardcolor = Colors.red;
                                        cardtext = snapshot.data[index].name +
                                            "   Account is private!";
                                      }
                                  }
                                  return Card(
                                      color: cardcolor,
                                      child: Container(
                                        height: 50,
                                        child: Row(
                                            mainAxisAlignment:
                                                MainAxisAlignment.spaceBetween,
                                            children: <Widget>[
                                              Padding(
                                                  padding:
                                                      EdgeInsets.only(left: 15),
                                                  child: Text(cardtext)),
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
                                                              color:
                                                                  Colors.red)),
                                                      child: Text(
                                                        'Romove From List',
                                                        style: TextStyle(
                                                            color:
                                                                Colors.white),
                                                      ),
                                                      color: Colors.red,
                                                      onPressed: () async {
                                                        final user =
                                                            Provider.of<User>(
                                                                context);
                                                        String userid =
                                                            user.uid;
                                                        Firestorecommands fc =
                                                            Firestorecommands();
                                                        dynamic results = await fc
                                                            .removetargetaccount(
                                                                userid,
                                                                snapshot
                                                                    .data[index]
                                                                    .name);
                                                        if (results ==
                                                            'success') {
                                                          final snackBar = SnackBar(
                                                              content: Text(
                                                                  'User Removed Successfuly.'));
                                                          Scaffold.of(context)
                                                              .showSnackBar(
                                                                  snackBar);
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
                                      ));
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
