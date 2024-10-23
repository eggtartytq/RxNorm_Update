# If your current Operating System SUPPORTS a GUI (Graphical User Interface).
# You should only fill the [mysql] or [postgresql] section the this configuration file. We will provide you with a
# User Interface to select your target DBMS, the target tables and files that you want to import into the database.

# If your current Operating System does NOT support a GUI (Graphical User Interface).
# You should complete all sections.
# For the [mysql] and [postgresql] sections, only fill in the one corresponding section to the DBMS you have chosen.

# DBMS Selection
# support: 'postgresql' or 'mysql', 'postgresql' is recommended
# Set as default value if GUI is supported
DBMS = 'postgresql'
# DB Connection Configuration
# # Test MySQL
# DB_USER = 'root'
# DB_PASSWORD = 'LewisQu738!'
# DB_DATABASE = 'rxnorm_allunique'
# DB_HOST = 'localhost'
# DB_PORT = 3306
# # Test PostgreSQL
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_DATABASE = 'rxnorm'
DB_HOST = 'localhost'
DB_PORT = 3306
# If using postgresel, set target schema name, default: public
# DB_TARGET_SCHEMA = 'public'

# Table Selection
# RXNCONSO: Concept Names and Sources in RxNorm
# RXNSAT: Simple Concept and Atom Attributes - that do not have a sub-element structure
# RXNSTY: The Semantic Type assigned to each concept
# RXNREL: Relationship between concepts or atoms known to RxNorm
# RXNCUICHANGES: Changes to the concept_id (RXCUI) for all atoms in RxNorm
# Set as default value if GUI is supported
TABLE = {'RXNCONSO','RXNSAT','RXNSTY','RXNREL','RXNCUICHANGES'}
# Only valid if GUI is not supported in your env
# File Selection Config file
FILE_PATH_CONFIG = 'file_path.txt'
