SELECT label, COUNT(*)
FROM workspace.silver.webpages
GROUP BY label;