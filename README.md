# Koru

## The ultimate employee management app for Ballet Companies

Koru is designed for use by the company manager/schedule maker.


Koru will allow you to upload both your current repertoire, and your employees(dancers, ballet masters, accompanists and repetiteurs).
You will then assign each employee their rehearsal responsibilities. When scheduling rehearsals, Koru will do the heavy lifting. You simply click on the rehearsal you want to schedule,
and koru will print out all employees involved. Koru will also alert you if an employee is scheduled for more than one rehearsal at a time.

Features:
User authentication
* Email check
* Password hashing
* Duplicate user check
Database:
* SQLAlchemy 
Account
* Password reset email
* Profile picture support
Access:
* Koru will only allow you to view your information
* Koru will stop you and abort if you try to access database items that belong to different users.