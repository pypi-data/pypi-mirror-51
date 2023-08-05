# jmpr

Tooling to permit AWS account navigation

### Note on paths:
AWS IAM fetch and create are carried out only using the name of an entity (user, group, role) by a client associated with an account.  Path does not play into AWS IAM entity retrieval or creation.

Paths are embedded in resulting entity ARN's, and ARNs are used to relate entities to each other, for instance in an 'assume role policy'.  In addition, paths can be used in policies to include or exclude.

So:
* Entities (users, roles, etc.) with the same name and different paths will collide
* Entities specified with an ARN that does not include the correct path will not be properly referenced.

Maintaining and managing YAML or JSON ARNs including path is likely to introduce frequent errors and failures.  

In consequence, the jmpr approach constructs entities in the way that they are fetched, by account and name, retaining any path information as decoration. 

When ARNs are needed for a call, the ARN is constructed dynamically in code from the attributes of the entity, which can include the path decoration.  This ensures consistent ARNs.

Initially in early release entity paths are guaranteed consistent and all equal to the asset_path, but in later releases entity-specific paths may be introduced so long as they are not embedded in ARNs.