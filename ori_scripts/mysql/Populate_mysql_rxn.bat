::
:: Database connection parameters
:: Please edit these variables to reflect your environment
::
 set MYSQL_HOME="c:\Program Files\MySQL\MySQL Server 8.0"
 set user=root
 set password=123456
 set host_name=localhost
 set db_name=rxnorm
 set max_error_count=0
 
 
 ATTRIB +R %logfile%   

echo ----------------------------------------
echo Starting ...
echo ----------------------------------------
echo.

%MYSQL_HOME%\bin\mysql -u %user%  -p%password% -h%host_name% --local-infile=1 %db_name% < Table_scripts_mysql_rxn.sql  >> mysql.log 2>&1

%MYSQL_HOME%\bin\mysql -u %user%  -p%password% -h%host_name%  --local-infile=1 %db_name% < Load_scripts_mysql_rxn_win.sql >> mysql.log 2>&1




echo
echo ----------------------------------------
echo Finished
echo ----------------------------------------
