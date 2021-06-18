echo Request Id?
read ID
QUERY="SELECT Id,Type AS Ty,User_Id AS Us,Approver_Id AS Ap,Status,CC_Id,uuid FROM Requests WHERE Id>=${ID}"
echo "${QUERY}"
USER=root
PASS=36MMySQLr00t1.,
SCHEMA=butler
COMMAND="mysql -t -v -B -u $USER -p$PASS -e '$QUERY' -D $SCHEMA"
echo ${COMMAND}
exec "$COMMAND"


