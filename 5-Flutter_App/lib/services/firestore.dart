import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:sociagrowapp/models/TargetAccounts.dart';
import 'package:sociagrowapp/models/Tasks.dart';

class Firestorecommands {
  final databaseReference = Firestore.instance;

  Future addnewuser(String uid) async {
    databaseReference.collection("UserSettings").document(uid).setData({
      'Taskperday': 30,
      'uid': uid,
      'addedtodatabase': false,
    });
  }

  Future addtargetaccount(String uid, String name) async {
    try {
      int len = 0;
      var docRef = await databaseReference
          .collection('TargetAccounts')
          .where('uid', isEqualTo: uid)
          .where('Targetname', isEqualTo: name)
          .getDocuments();
      docRef.documents.forEach((documents) {
        len++;
      });
      if (len >= 1) {
        return 'Exists';
      }
      len = 0;
      docRef = await databaseReference
          .collection('TargetAccounts')
          .where('uid', isEqualTo: uid)
          .getDocuments();
      docRef.documents.forEach((documents) {
        len++;
      });
      if (len >= 50) {
        return 'Toomany';
      }

      await databaseReference
          .collection("TargetAccounts")
          .add({'uid': uid, 'Targetname': name, 'Status': 0});
      return 'success';
    } catch (e) {
      print('Fail');
      return Null;
    }
  }

  Future gettargetaccountslist(String uid) async {
    try {
      List<TargetAccount> targetaccounts = [];
      var docRef = await databaseReference
          .collection('TargetAccounts')
          .where('uid', isEqualTo: uid)
          .getDocuments();
      docRef.documents.forEach((documents) {
        targetaccounts.add(TargetAccount(
            documents.data['Targetname'], documents.data['Status']));
      });
      return targetaccounts;
    } catch (e) {
      return Null;
    }
  }

  Future removetargetaccount(String uid, String name) async {
    try {
      var docRef = await databaseReference
          .collection('TargetAccounts')
          .where('uid', isEqualTo: uid)
          .where('Targetname', isEqualTo: name)
          .getDocuments();
      docRef.documents.forEach((documents) {
        documents.reference.delete();
      });
      return 'success';
    } catch (e) {
      return Null;
    }
  }

  Future getaccounttasks(String uid) async {
    try {
      List<Tasks> tasks = [];
      var docRef = await databaseReference
          .collection('Tasks')
          .where('uid', isEqualTo: uid)
          .where('Done', isEqualTo: false)
          .getDocuments();
      docRef.documents.forEach((documents) {
        tasks.add(Tasks(
            documents.data['Account'],
            documents.data['Task'],
            documents.data['Likepercentage'],
            documents.data['TargetAccount'],
            documents.documentID));
      });
      return tasks;
    } catch (e) {}
  }

  Future completetasks(String docid) async {
    try {
      await databaseReference
          .collection('Tasks')
          .document(docid)
          .setData({'Done': true}, merge: true);
      return 'success';
    } catch (e) {
      print('err');
      return Null;
    }
  }

  Future tasksnum(String uid) async {
    try {
      var docRef = await databaseReference
          .collection('UserSettings')
          .document(uid)
          .get();

      return docRef.data['Taskperday'];
    } catch (e) {
      print('err');
      return Null;
    }
  }

  

  Future changetasksnum(String uid, int number) async {
    try {
      await databaseReference
          .collection('UserSettings')
          .document(uid)
          .setData({'Taskperday': number}, merge: true);

      return 'success';
    } catch (e) {
      print('err');
      return Null;
    }
  }

  
}
