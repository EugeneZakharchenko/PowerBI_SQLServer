-- IMPLEMENTING ROW LEVEL SECURITY IN SQL SERVER

CREATE LOGIN CHINA WITH PASSWORD = 'CHINA'
CREATE LOGIN BRAZIL WITH PASSWORD = 'BRAZIL'
CREATE LOGIN US WITH PASSWORD = 'US'

CREATE USER VINET FOR LOGIN CHINA
CREATE USER TOMPS FOR LOGIN BRAZIL
CREATE USER HANAR FOR LOGIN US

-- Create roles for users
CREATE ROLE CHINA;
CREATE ROLE BRAZIL;
CREATE ROLE US;

-- Assign users to roles
ALTER ROLE CHINA ADD MEMBER VINET;
ALTER ROLE BRAZIL ADD MEMBER TOMPS;
ALTER ROLE US ADD MEMBER HANAR;

-- Define Role-Based Access
CREATE FUNCTION dbo.fn_securitypredicate(@Country AS NVARCHAR(50))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS fn_securitypredicate_result
WHERE
   (@Country = 'China' AND USER_NAME() = 'VINET')
   OR
   (@Country = 'US' AND USER_NAME() = 'HANAR')
   OR
   (@Country = 'Brazil' AND USER_NAME() = 'TOMPS')
   OR
   (USER_NAME() = 'dbo');

-- Create a security policy that enforces the row-level security based on the roles
CREATE SECURITY POLICY CountrySecurityPolicy
ADD FILTER PREDICATE dbo.fn_securitypredicate(Country) ON dbo.EmployeeSampleData
WITH (STATE = ON);

-- Grant access to the table
GRANT SELECT ON EmployeeSampleData TO VINET
GRANT SELECT ON EmployeeSampleData TO HANAR
GRANT SELECT ON EmployeeSampleData TO TOMPS
GRANT SELECT, UPDATE, INSERT and DELETE TO dbo


SELECT CURRENT_USER


EXECUTE AS USER = 'HANAR'
SELECT * FROM EmployeeSampleData
