# Bloomia General Socket Server

## What GSS is responsible for?

GSS is responsible for updating, adding, deleting managing all user data. It's also responsible for all AI chat system users using. Basically it handless almost 90% of use cases about file editor management, synchronization and AI logic happens between user and Bloomia servers.

## Read before diving to source code

- Almost every socket.io handler takes a "transactionId" as an input. This transactionId is coming from client and when transaction - or event - is successful, server sends an success message with its "transactionId". This allows client to see what changes are successful and how much time took since last transaction changes to be applied.
