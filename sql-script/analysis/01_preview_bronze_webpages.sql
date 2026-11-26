-- Step 6: Verify ingested data
-- Preview the bronze table contents.
SELECT *
FROM workspace.bronze.webpages
LIMIT 10;
