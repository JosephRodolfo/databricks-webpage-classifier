-- Step 6: Verify ingested data
-- Check the distribution of positive and negative examples.
SELECT
    label,
    COUNT(*) AS document_count
FROM workspace.bronze.webpages
GROUP BY label;
