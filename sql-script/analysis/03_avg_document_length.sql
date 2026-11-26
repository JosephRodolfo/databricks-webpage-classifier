-- Step 6: Verify ingested data
-- Check the average document length per label.
SELECT
    label,
    AVG(LENGTH(text)) AS avg_document_length
FROM workspace.bronze.webpages
GROUP BY label;
