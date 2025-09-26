import boto3
from boto3_dataclass_iam import iam_caster

# Use boto3 normally
iam_client = boto3.client("iam")
response = iam_client.get_role(RoleName="MyRole")

# Convert to structured dataclass
response = iam_caster.get_role(response)
# Now you get full IDE autocompletion and type safety!
# IDE shows available attributes

print(response.Role)